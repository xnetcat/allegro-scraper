from itertools import cycle
import logging
from random import random
import requests

from allegro.search.product import Product
from allegro.parsers.offer import is_captcha_required
from bs4 import BeautifulSoup
from typing import List, Optional, Tuple


def parse_website(url: str, proxy: str = None):
    # Default headers
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36", # noqa: E501
        "Referer": "https://allegro.pl",
        "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9,pl;q=0.8",
        "Sec-Fetch-Dest": "image",
        "Sec-Fetch-Mode": "no-cors",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Gpc": "1"
    }

    # Create proxies object
    if proxy is not None:
        proxies = {"http": f"https://{proxy}", "https": f"https://{proxy}"}
    else:
        proxies = None

    # Send http GET request
    request = requests.get(
        url,
        headers=headers,
        proxies=proxies,
    )

    # Parse html with BeautifulSoup
    soup = BeautifulSoup(request.text, "html.parser")

    # return soup
    return soup


def parse_products(
    search_term: str,
    query_string: str = "",
    page_num: int = 1,
    proxies: List[str] = None,
    avoid_duplicates: bool = None,
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

    # Proxy cycle vars
    proxy_cycle = None
    start_proxy = None
    proxy = None

    # Init proxy cycle
    if proxies is not None:
        proxy_cycle = cycle(proxies)
        proxy = next(proxy_cycle)

    try:
        # parse website
        soup = parse_website(url, proxy)
    except ValueError as e:
        if proxy_cycle is not None:
            # while loop acts like a do while
            while True:
                try:
                    # parse website
                    soup = parse_website(url, proxy)
                except ValueError:
                    proxy = next(proxy_cycle)
        else:
            logging.error("Couldn't parse website")
            raise e

    # Check for captcha
    if is_captcha_required(soup):
        raise ValueError("Captcha is required")

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

    # FIXME: Proxy cycling is probaly not working
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
            if proxy_cycle is not None and proxy is not None:
                while True:
                    try:
                        product = Product.from_url(
                            url=product_url, proxy=proxy, timeout=timeout
                        )
                        break
                    except ValueError:
                        logging.info("Changing proxy")
                        next(proxy_cycle)
            else:
                product = Product.from_url(
                    url=product_url, timeout=timeout
                )

            # TODO: NOT TESTED
            if avoid_duplicates is True and product.url in (
                prod.url for prod in products
            ):
                continue

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

    # Return list with products
    return products, True
