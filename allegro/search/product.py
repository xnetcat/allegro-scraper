import json
import requests

from typing import List
from dataclasses import dataclass
from bs4 import BeautifulSoup

from allegro.parsers.offer import (
    _find_product_category,
    _find_product_images,
    _find_product_name,
    _find_product_parameters,
    _find_product_price,
    _find_product_quantity,
    _find_product_rating,
    _find_product_seller,
    _is_buynow_offer,
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
    def from_url(cls, url, proxy=None):
        """
        ### Args
        - url: `str` a url of a product that we want to scrape

        ### Returns
        - `Product` that contains the metadata of a product.
        """
        if "allegro.pl/oferta" not in url:
            if (
                "allegro.pl/events/clicks" not in url
                and "&redirect=https%3A%2F%2Fallegro.pl%2Foferta" not in url
            ):
                raise Exception(f"Passed url is not that of a product: {url}")

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
            url,
            headers=headers,
            proxies=proxy,
        )

        # Parse html with BeautifulSoup
        soup = BeautifulSoup(request.text, "html.parser")

        if not _is_buynow_offer(soup):
            raise NotImplementedError("Auctions and advertisements are not supported")

        # Find name in parsed website
        name = _find_product_name(soup)

        # Find price in parsed website
        price = _find_product_price(soup)

        # Find category in parsed website
        category = _find_product_category(soup)

        # Find seller in parsed website
        seller = _find_product_seller(soup)

        # Find quantity in parsed website
        quantity = _find_product_quantity(soup)

        # Find rating in parsed website
        rating = _find_product_rating(soup)

        # Find images in parsed website
        images = _find_product_images(soup)

        # Find parameters in parsed website
        parameters = _find_product_parameters(soup)

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
