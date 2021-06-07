import logging

from allegro.search.product import Product
from allegro.types.crawler import Filters, Options
from allegro.constants import FILTERS
from allegro.parsers.crawler import parse_website
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

    soup = parse_website(f"https://allegro.pl/listing?string={search_term}", proxies)

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
    products_number = len(sections)

    logging.info(f"Found {products_number} products")
    for index, section in enumerate(sections):
        # Find url to product in a tag
        product_link = section.find("a", attrs={"rel": "nofollow", "tabindex": "-1"})

        # Create product object using url
        product = Product.from_url(product_link.get("href"))

        # Display what product we are scraping
        if logging.DEBUG >= logging.root.level:
            logging.debug(
                f'Scraping "{product.name}" with url "{product.url}" '
                "[{index + 1}/{products_number}]"
            )
        else:
            logging.info(f'Scraping "{product.name}" [{index + 1}/{products_number}]')

        # Add product to list
        products.append(product)

    # Return list with products
    return products


def crawl(
    search_term: str,
    options: Options = None,
    filters: Filters = None,
    proxies: dict = None,
) -> List[Product]:
    """
    ### Args
    - search_term: `str` name of the searched item
    - options: `Options` search options
    - filters: `Filters` product filters
    - proxies: `dict` dictionary containing proxies

    ### Returns
    - `List[Product]` list containing scrapped products
    """

    # No options so we default to results from first page
    if options is None and filters is None:
        logging.warning("No options and filters, scraping only first page")
        return search(search_term)

    # List containing query filters for product
    query = []

    # Products list
    products = []

    if filters is not None:
        for index, (key, value) in enumerate(filters.items()):
            # skip filters with None value
            if value is None:
                continue

            if type(value) == bool and value is True:
                query.append(FILTERS[key])
            elif type(value) == list:
                # we know that value is a list
                query.extend([FILTERS[key][val] for val in value])  # type: ignore
            elif type(FILTERS[key]) == function:
                query.append(FILTERS[key](value))
            elif type(value) == str:
                if FILTERS[key] is not None:
                    query.append(FILTERS[key])

    # Create query string
    if len(query) >= 1:
        query_string = "&".join(query).replace(" ", "%20")
    else:
        query_string = ""

    soup = parse_website(
        f"https://allegro.pl/listing?string={search_term}{query_string}", proxies
    )

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
    products_number = len(sections)

    logging.info(f"Found {products_number} products")
    for index, section in enumerate(sections):
        # Find url to product in a tag
        product_link = section.find("a", attrs={"rel": "nofollow", "tabindex": "-1"})

        # Create product object using url
        product = Product.from_url(product_link.get("href"))

        # Display what product we are scraping
        if logging.DEBUG >= logging.root.level:
            logging.debug(
                f'Scraping "{product.name}" with url "{product.url}" '
                "[{index + 1}/{products_number}]"
            )
        else:
            logging.info(f'Scraping "{product.name}" [{index + 1}/{products_number}]')

        # Add product to list
        products.append(product)

    # Return list with products
    return products
