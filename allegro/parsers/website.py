import logging
import requests

from itertools import cycle
from bs4 import BeautifulSoup
from typing import List, Optional, Tuple
from allegro.search.product import Product
from allegro.parsers.offer import is_captcha_required


def parse_website(url: str, proxies: List[str] = None, timeout: int = None):
    # Init proxy cycle
    if proxies is not None and len(proxies) >= 1:
        proxy_cycle = cycle(proxies)
        current_proxy = next(proxy_cycle)
        start_proxy = current_proxy
        proxy_object = {
            "http": f"https://{current_proxy}",
            "https": f"https://{current_proxy}",
        }
    else:
        proxy_cycle = None
        current_proxy = None
        start_proxy = None
        proxy_object = None

    # try to get soup
    soup = get_soup_check(url, proxies=proxy_object, timeout=timeout)

    # captcha is required
    if soup is None:
        # Proxy failed so we change proxy
        if proxy_cycle is not None:
            current_proxy = next(proxy_cycle)
            logging.debug(f'Changing proxy to "{current_proxy}"')

        while True:
            if proxy_cycle is not None and current_proxy is not None:
                # We've run out of proxies to use
                if start_proxy == current_proxy:
                    raise OSError("We can't bypass IP block")

                # Update proxy object
                proxy_object = {
                    "http": f"https://{current_proxy}",
                    "https": f"https://{current_proxy}",
                }

                # Get soup
                soup = get_soup_check(url=url, proxies=proxy_object)

                # soup is fine return it
                if soup is not None:
                    return soup
                else:
                    # Soup is wrong, try again
                    current_proxy = next(proxy_cycle)
                    logging.debug(f'Changing proxy to "{current_proxy}"')
            else:
                raise OSError("You are being IP restricted, please use proxies")
    else:
        # soup is fine return it
        return soup


def get_soup_check(
    url: str, proxies: dict = None, timeout: int = None
) -> Optional[BeautifulSoup]:
    # Default headers
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",  # noqa: E501
        "Referer": "https://allegro.pl",
        "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9,pl;q=0.8",
        "Sec-Fetch-Dest": "image",
        "Sec-Fetch-Mode": "no-cors",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Gpc": "1",
    }

    try:
        # Send http GET request
        request = requests.get(url, headers=headers, proxies=proxies, timeout=timeout)
    except:
        return None

    # Parse website
    soup = BeautifulSoup(request.text, "html.parser")

    if is_captcha_required(soup):
        return None
    else:
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

    # try to parse website
    soup = parse_website(url, proxies)

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
            product = Product.from_url(
                url=product_url, proxies=proxies, timeout=timeout
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
