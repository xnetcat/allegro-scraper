import requests
import logging

from bs4 import BeautifulSoup
from allegro.search.product import Product
from allegro.types.types_crawler import Parameters, Options
from typing import List

PARAMETERS = {
    "smart_free_shipping": "allegro-smart-standard=1",
    "product_condition": {
        "new": "stan=nowe",
        "used": "stan=używane",
        "incomplete_set": "stan=niepełny komplet",
        "new_without_tags": "stan=nowe bez metki",
        "new_with_defect": "stan=nowe z defektem",
        "after_return": "stan=po zwrocie",
        "aftermarket": "stan=powystawowe",
        "regenerated": "stan=regenerowane",
        "damaged": "stan=uszkodzone",
        "refurbished": "stan=odnowione przez sprzedawcę",
        "for_renovation": "stan=do renowacji",
        "not_requiring_renovation": "stan=niewymagające renowacji",
    },
    "offer_type": {
        "buy_now": "offerTypeBuyNow=1",
        "auction": "offerTypeAuction=2",
        "advertisement": "offerTypeAdvert=3",
    },
    "price_min": lambda value: f"price_from={str(value)}",
    "price_max": lambda value: f"price_to={str(value)}",
    "delivery_time": {
        "today": "delivery_time=today",
        "one_day": "delivery_time=one_day",
        "two_day": "delivery_time=two_days",
    },
    "delivery_methods": {
        "courier": "dostawa-kurier=1",
        "inpost_parcel_locker": "dostawa-paczkomaty-inpost=1",
        "overseas_delivery": "dostawa-dostawa-za-granice=1",
        "pickup_at_the_point": "dostawa-odbior-w-punkcie=1",
        "letter": "dostawa-list=1",
        "package": "dostawa-paczka=1",
        "pickup": "dostawa-odbior-osobisty=1",
        "email": "dostawa-przesylka-elektroniczna=1",
    },
    "delivery_options": {
        "free_shipping": "freeShipping=1",
        "free_return": "freeReturn=1",
    },
}


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
                '[{index + 1}/{products_number}]'
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
    parameters: Parameters = None,
    proxies: dict = None,
) -> List[Product]:
    """
    ### Args
    - search_term: `str` name of the searched item
    - options: `Options` search options
    - parameters: `Parameters` product parameters
    - proxies: `dict` dictionary containing proxies

    ### Returns
    - `List[Product]` list containing scrapped products
    """

    # No options so we default to results from first page
    if options is None and parameters is None:
        logging.warning("No options and parameters, scraping only first page")
        return search(search_term)

    # List containing query parameters for product
    query = []

    if parameters is not None:
        for index, (key, value) in enumerate(parameters.items()):
            # skip parameters with None value
            if value is None:
                continue

            if type(value) == bool and value is True:
                query.append(PARAMETERS[key])
            elif type(value) == list:
                # we know that value is a list
                query.extend([PARAMETERS[key][val] for val in value])  # type: ignore
            elif type(value) == float and "price" in key:
                # we know that PARAMETERS[key] is a lambda function
                query.append(PARAMETERS[key](value))  # type: ignore
            elif type(value) == str:
                query.append(PARAMETERS[key])

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

    # init query string
    query_string = ""

    # join all query parameters
    for param in query:
        # param is string
        query_string += f"&{param.replace(' ', '%20')}"  # type: ignore

    # Send http GET request
    request = requests.get(
        f"https://allegro.pl/listing?string={search_term}{query_string}",
        headers=headers,
        proxies=proxies,
    )

    # Parse html with BeautifulSoup
    soup = BeautifulSoup(request.text, "html.parser")

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
                '[{index + 1}/{products_number}]'
            )
        else:
            logging.info(f'Scraping "{product.name}" [{index + 1}/{products_number}]')

        # Add product to list
        products.append(product)

    # Return list with products
    return products
