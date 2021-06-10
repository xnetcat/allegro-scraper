import logging

from typing import List, Optional, Tuple
from allegro.utils import get_soup
from allegro.search import Product


def parse_products(
    search_term: str,
    query_string: str = "",
    page_num: int = 1,
    proxies: List[str] = None,
    max_results: int = None,
    timeout: int = None,
) -> Optional[Tuple[List[Product], bool]]:
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

    for index, section in enumerate(sections):
        index += 1

        # max products
        if max_results == len(products):
            return products, False

        # Find url to product in a tag
        product_link = section.find("a", attrs={"rel": "nofollow", "tabindex": "-1"})
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
            continue

    pagination_input = soup.find(
        "input", attrs={"data-role": "page-number-input", "data-page": True}
    )

    last_page = int(pagination_input.get("data-maxpage"))

    if page_num == last_page:
        logging.info("Reached last page, stopping")
        return products, False

    # Return list with products
    return products, True
