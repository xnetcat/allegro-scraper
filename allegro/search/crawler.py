import logging

from typing import List
from types import FunctionType
from allegro.parsers.website import parse_products, parse_website
from allegro.types.options import Options
from allegro.constants import FILTERS
from allegro.search.product import Product
from allegro.types.filters import Filters


def search(search_term: str, proxy: dict = None) -> List[Product]:
    """
    ### Args
    - search_term: `str` name of the searched item

    ### Returns
    - `List[Product]` list containing scrapped products
    """

    # Products list
    products = []

    # url create url and encode spaces
    url = f"https://allegro.pl/listing?string={search_term}".replace(" ", "%20")

    soup = parse_website(url, proxy)

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

        logging.info(
            f'Scraping "{product.name}"'
            f'{f" with url {product.url}" if logging.DEBUG >= logging.root.level else ""}'
            f" [{index + 1}/{products_number}]"
        )

        # Add product to list
        products.append(product)

    # Return list with products
    return products


def crawl(
    search_term: str,
    options: Options = None,
    filters: Filters = None,
    proxy: dict = None,
) -> List[Product]:
    """
    ### Args
    - search_term: `str` name of the searched item
    - options: `Options` search options
    - filters: `Filters` product filters
    - proxy: `dict` dictionary containing proxy

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

    # init empty query string
    query_string = ""

    if filters is not None:
        for index, (key, value) in enumerate(filters.items()):
            # skip filters with None value
            if value is None:
                continue

            if type(value) == bool and value is True:
                query.append(FILTERS[key])
            elif type(value) == list:
                query.extend([FILTERS[key][val] for val in value])  # type: ignore
            elif type(FILTERS[key]) == FunctionType:  # type: ignore
                query.append(FILTERS[key](value))  # type: ignore
            elif type(value) == str:
                if FILTERS[key][value] is not None:  # type: ignore
                    query.append(FILTERS[key][value])  # type: ignore
            else:
                logging.warning(f"Unhandled type {type(value)} of value {value}")

        # Create query string
        if len(query) >= 1:
            for q in query:
                query_string += f"&{q}"

    if options is not None:
        start_page = options.get("start_page")
        pages_to_fetch = options.get("pages_to_fetch")
        max_results = options.get("max_results")
        avoid_duplicates = options.get("avoid_duplicates")
    else:
        start_page = None
        pages_to_fetch = None
        max_results = None
        avoid_duplicates = None

    if start_page is None:
        start_page = 1

    if max_results is not None:
        logging.info(f"Max results {max_results}")

    if pages_to_fetch is not None:
        logging.info(f"Will fetch {pages_to_fetch} pages")
        for page_num in range(start_page, pages_to_fetch + 1):
            logging.info(f"Fetching {page_num} page")

            # Fetch offers
            offers = parse_products(
                search_term=search_term,
                page_num=page_num,
                query_string=query_string,
                max_results=max_results - len(products)
                if max_results is not None
                else None,
                avoid_duplicates=avoid_duplicates,
                proxy=proxy,
            )

            # add new products to products list
            products.extend(offers[0])

            # Stop crawling
            if offers[1] is False:
                break
    else:
        # Start number
        page_num = start_page

        # Start loop
        while True:
            offers = parse_products(
                search_term=search_term,
                query_string=query_string,
                page_num=page_num,
                max_results=max_results,
                proxy=proxy,
            )

            # add new products to products list
            products.extend(offers[0])

            # Stop crawling
            if offers[1] is False:
                break

            # increase page num
            page_num += 1

    # return products
    return products
