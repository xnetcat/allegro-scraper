import json
import requests

from dataclasses import dataclass
from typing import List
from bs4 import BeautifulSoup
from allegro.parsers.product import (
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

        request = requests.get(url, proxies=proxy, headers=headers)
        soup = BeautifulSoup(request.text, "html.parser")

        if not _is_buynow_offer(soup):
            raise NotImplementedError("Auctions and advertisements are not supported")

        name = _find_product_name(soup)
        price = _find_product_price(soup)
        category = _find_product_category(soup)
        seller = _find_product_seller(soup)
        quantity = _find_product_quantity(soup)
        rating = _find_product_rating(soup)
        images = _find_product_images(soup)
        parameters = _find_product_parameters(soup)

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

        data_dict = json.loads(data)

        return cls(**data_dict)
