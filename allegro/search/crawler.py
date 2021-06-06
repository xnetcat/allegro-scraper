import requests
import logging

from bs4 import BeautifulSoup
from allegro.search.product import Product
from allegro.types.crawler import Options
from typing import List


def search(search_term: str, proxies: dict = None) -> List[Product]:
    """
    ### Args
    - search_term: `str` name of the searched item

    ### Returns
    - `List[Product]` list containing scrapped products
    """

    # Products list
    products = []

    # Default headers
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0",  # noqa: E501
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
    }

    # Send http GET request
    request = requests.get(
        f"https://allegro.pl/listing?string={search_term}",
        headers=headers,
        proxies=proxies,
    )

    # Parse html with BeautifulSoup
    soup = BeautifulSoup(request.text, "html.parser")

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

    logging.info(f"Found {len(sections)} products")
    for index, section in enumerate(sections):
        product_link = section.find("a", attrs={"rel": "nofollow", "tabindex": "-1"})
        product = Product.from_url(product_link.get("href"))

        if logging.DEBUG >= logging.root.level:
            logging.debug(
                f'Scraping "{product.name}" with url "{product.url}" [{index + 1}/{len(sections)}]'
            )
        else:
            logging.info(f'Scraping "{product.name}"' f" [{index + 1}/{len(sections)}]")

        # Add product to list
        products.append(product)

    # Return list with products
    return products


def crawl(
    search_term: str,
    options: Options = None,
    proxies: dict = None,
) -> List[Product]:
    """
    ### Args
    - search_term: `str` name of the searched item
    - options: `Options` search options

    ### Returns
    - `List[Product]` list containing scrapped products
    """

    # No options so we default to results from first page
    if options is None:
        return search(search_term)

    # Products list
    products = []

    # Default headers
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0",  # noqa: E501
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
    }

    # Send http GET request
    request = requests.get(
        f"https://allegro.pl/listing?string={search_term}",
        headers=headers,
        proxies=proxies,
    )

    # Parse html with BeautifulSoup
    soup = BeautifulSoup(request.text, "html.parser")
