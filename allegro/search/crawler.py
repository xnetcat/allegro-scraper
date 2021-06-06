import requests
import logging

from bs4 import BeautifulSoup
from allegro.search.product import Product
from typing import List


def search(search_term: str, proxies=None) -> List[Product]:
    """
    ### Args
    - search_term: `str` name of the searched item

    ### Returns
    - `List[Product]` list containing scrapped products
    """
    products = []
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

    req = requests.get(
        f"https://allegro.pl/listing?string={search_term}",
        headers=headers,
        proxies=proxies,
    )
    soup = BeautifulSoup(req.text, "html.parser")

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
                f'Scraping "{product.name}" with url "{product.url}" [{index + 1}/{len(sections) - 1}]'
            )
        else:
            logging.info(f'Scraping "{product.name}" [{index + 1}/{len(sections) - 1}]')

        # Add product to list
        products.append(product)

    # Return list with products
    return products
