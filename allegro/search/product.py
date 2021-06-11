from concurrent.futures import thread
import logging
import json

import concurrent.futures
from dataclasses import dataclass
from typing import List, Tuple
from allegro.utils import get_soup
from allegro.parsers import (
    find_product_category,
    find_product_images,
    find_product_name,
    find_product_parameters,
    find_product_price,
    find_product_quantity,
    find_product_rating,
    find_product_seller,
    is_buynow_offer,
)


@dataclass(frozen=True)
class Product:
    """
    ### Overview
    - Contains the parameters of a product.

    ### Public attributes
    - url: `str` url of a product
    - name: `str` name of the product
    - price: `float` price of a product
    - category: `str` category url
    - seller: `str` seller id
    - quantity: `int` number of products left
    - rating: `float` product rating
    - images: `List[str]` array of images, first item in the array is the main image
    - parameters: `dict` product parameters
    """

    url: str
    name: str
    category: str
    price: float
    seller: str
    quantity: int
    rating: float
    images: List[str]
    parameters: dict

    @classmethod
    def from_url(cls, url: str, proxies: List[str] = None, timeout: int = None):
        """
        ### Args
        - url: `str` a url of a product that we want to scrape
        - proxies: `List[str]` proxies list

        ### Returns
        - `Product` that contains the metadata of a product.
        """
        if "allegro.pl/oferta" not in url:
            if (
                "allegro.pl/events/clicks" not in url
                and "&redirect=https%3A%2F%2Fallegro.pl%2Foferta" not in url
            ):
                raise ValueError(f"Passed url is not that of a product: {url}")

        # try to parse product
        soup = get_soup(url=url, proxies=proxies, timeout=timeout)

        if is_buynow_offer(soup) is False:
            raise NotImplementedError("Auctions and advertisements are not supported")

        # Find name in parsed website
        name = find_product_name(soup)

        # Find price in parsed website
        price = find_product_price(soup)

        # Find category in parsed website
        category = find_product_category(soup)

        # Find seller in parsed website
        seller = find_product_seller(soup)

        # Find quantity in parsed website
        quantity = find_product_quantity(soup)

        # Find rating in parsed website
        rating = find_product_rating(soup)

        # Find images in parsed website
        images = find_product_images(soup)

        # Find parameters in parsed website
        parameters = find_product_parameters(soup)

        # Return product object
        return cls(
            url, name, category, price, seller, quantity, rating, images, parameters
        )

    @classmethod
    def from_data_dump(cls, data: str):
        """
        ### Args
        - data: `str`, a string conataining all the necessary data used to create a
                       Product object. It's provided by the `get_data_dump` method.

        ### Returns
        - `Product` that contains the metadata of a product.
        """

        # Create dict frm json string
        data_dict = json.loads(data)

        # Return product object
        return cls(**data_dict)


def parse_products(
    search_term: str,
    query_string: str = "",
    page_num: int = 1,
    proxies: List[str] = None,
    max_results: int = None,
    timeout: int = None,
    threads: int = None,
) -> Tuple[List[Product], bool]:
    # create url and encode spaces
    url = (
        f"https://allegro.pl/listing?string={search_term}"
        f"{query_string}&p={str(page_num)}".replace(" ", "%20")
    )

    # Current product
    product = None

    # try to parse website
    soup = get_soup(url, proxies)

    # Products list
    products: List[Product] = []

    # Find all products on a page, each section is one product
    sections = soup.find_all(
        "article",
        attrs={
            "data-role": "offer",
            "data-analytics-view-custom-index0": True,
            "data-analytics-view-custom-deliverylabel": True,
            "data-analytics-view-custom-page": True,
            "data-analytics-view-value": True,
        },
    )

    # Number of products found
    sections_len = len(sections)

    if max_results is not None and sections_len > max_results:
        logging.info(
            f"Found {sections_len} products, but only scraping {max_results} products"
        )
    else:
        logging.info(f"Found {sections_len} products")

    if threads is not None:
        products_urls = []
        for section in sections:
            # max products
            if max_results != len(products_urls):
                # Find url to product in a tag
                product_link = section.find(
                    "a", attrs={"rel": "nofollow", "tabindex": "-1"}
                )
                product_url = product_link.get("href")
                products_urls.append(product_url)

        # Threadding magic
        with concurrent.futures.ProcessPoolExecutor(max_workers=5) as executor:
            future_to_product = {
                executor.submit(Product.from_url, urll, proxies, timeout): urll
                for urll in products_urls
            }
            for index, future in enumerate(
                concurrent.futures.as_completed(future_to_product)
            ):
                index = index + 1

                # Start future
                future_to_product[future]

                if max_results is not None:
                    if max_results > sections_len:
                        print_num = sections_len
                    else:
                        print_num = max_results
                else:
                    print_num = sections_len

                # Try to get product
                try:
                    product = future.result()

                    # Add product to products list
                    products.append(product)
                    logging.info(
                        f'Scrapped "{product.name}"'
                        f'{f" with url {product.url}" if logging.DEBUG >= logging.root.level else ""}'
                        f" [{index}/{print_num}]"
                    )

                    # We've hit max results so we return products
                    if max_results == len(products):
                        return products, False
                # Advert and auction
                except NotImplementedError:
                    logging.info(
                        f'Ignoring "{products_urls[index]}" '
                        "because it's advert or auction "
                        f"[{index}/{print_num}]"
                    )

            # Shutdown executor, not sure if needed but I will leave it
            executor.shutdown(wait=True)
    else:
        for index, section in enumerate(sections):
            index += 1

            # max products
            if max_results == len(products):
                return products, False

            # Find url to product in a tag
            product_link = section.find(
                "a", attrs={"rel": "nofollow", "tabindex": "-1"}
            )
            product_url = product_link.get("href")

            if max_results is not None:
                if max_results > sections_len:
                    print_num = sections_len
                else:
                    print_num = max_results
            else:
                print_num = sections_len

            # Create product object using url
            try:
                product = Product.from_url(
                    url=product_url, proxies=proxies, timeout=timeout
                )

                logging.info(
                    f'Scraping "{product.name}"'
                    f'{f" with url {product.url}" if logging.DEBUG >= logging.root.level else ""}'
                    f" [{index}/{print_num}]"
                )

                # Add product to list
                products.append(product)
            # Ignore adverts and auctions
            except NotImplementedError:
                logging.info(
                    f'Ignoring "{product_link}" '
                    "because it's advert or auction "
                    f"[{index}/{print_num}]"
                )

    pagination_input = soup.find(
        "input", attrs={"data-role": "page-number-input", "data-page": True}
    )

    last_page = int(pagination_input.get("data-maxpage"))

    if page_num == last_page:
        logging.info("Reached last page, stopping")
        return products, False

    # Return list with products
    return products, True
