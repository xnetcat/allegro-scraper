import logging

from typing import List
from types import FunctionType
from allegro.constants import FILTERS
from allegro.types import Filters, Options
from allegro.utils import get_soup
from allegro.search.product import parse_products, Product


def search(
    search_term: str, options: Options = None, proxies: List[str] = None
) -> List[Product]:
    """
    ### Args
    - search_term: `str` name of the searched item

    ### Returns
    - `List[Product]` list containing scrapped products
    """

    # Products list
    products = []

    # Current product
    product = None

    # Set settings
    if options is not None:
        timeout = options.get("request_timeout")
    else:
        timeout = None

    # create url and encode spaces
    url = f"https://allegro.pl/listing?string={search_term}".replace(" ", "%20")

    # Try to parse url
    soup = get_soup(url=url, proxies=proxies)

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

        try:
            product = Product.from_url(
                url=product_link.get("href"), proxies=proxies, timeout=timeout
            )
        except ValueError as e:
            raise e
        except NotImplementedError:
            logging.info(
                f'Ignoring "{product_link}" '
                "because it's advert or auction "
                f"[{index + 1}/{products_number}]"
            )
            continue

        if product is not None:
            if logging.DEBUG >= logging.root.level:
                message = (
                    f'Scraping "{product.name}" '
                    f'with url "{product.url}" '
                    f"[{index + 1}/{products_number}]"
                )
            else:
                message = (
                    f'Scraping "{product.name}" ' f"[{index + 1}/{products_number}]"
                )

            logging.info(message)

            # Add product to list
            products.append(product)

    # Return list with products
    return products


def crawl(
    search_term: str,
    options: Options = None,
    filters: Filters = None,
    proxies: List[str] = None,
) -> List[Product]:
    """
    ### Args
    - search_term: `str` name of the searched item
    - options: `Options` search options
    - filters: `Filters` product filters
    - proxies: `List[str]` dictionary containing proxy

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
    products: List[Product] = []

    # init empty query string
    query_string = ""

    if filters is not None:
        for key, value in filters.items():
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
        timeout = options.get("request_timeout")
        threads = options.get("threads")
    else:
        start_page = None
        pages_to_fetch = None
        max_results = None
        timeout = None
        threads = None

    remaining_items = None

    if start_page is None:
        start_page = 1

    if max_results is not None:
        logging.info(f"Max results {max_results}")

    if pages_to_fetch is not None:
        logging.info(f"Will fetch {pages_to_fetch} pages")

        for page_num in range(start_page, pages_to_fetch + 1):
            # TODO: CHECK IF WE'VE REACHED LAST PAGE
            logging.info(f"Fetching {page_num} page")

            if max_results is not None:
                remaining_items = max_results - len(products)

            # Fetch offers
            offers = parse_products(
                search_term=search_term,
                page_num=page_num,
                query_string=query_string,
                proxies=proxies,
                timeout=timeout,
                max_results=remaining_items,
                threads=threads
            )

            # add new products to products list
            products.extend(offers[0])

            logging.info(f"Fetched {len(products)} products from {page_num} pages")

            # Stop crawling
            if offers[1] is False:
                break
    else:
        # Start number
        page_num = start_page

        # Start loop
        while True:
            # Fetch offers
            offers = parse_products(
                search_term=search_term,
                page_num=page_num,
                query_string=query_string,
                proxies=proxies,
                timeout=timeout,
                max_results=max_results,
                threads=threads
            )

            # add new products to products list
            products.extend(offers[0])

            logging.info(f"Fetched {len(products)} products from {page_num} pages")

            # Stop crawling
            if offers[1] is False:
                break

            # increase page num
            page_num += 1

    # return products
    return products
