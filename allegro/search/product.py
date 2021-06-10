import json

from typing import List
from dataclasses import dataclass

from allegro.utils import get_soup
from allegro.parsers import (
    find_product_category,
    find_product_images,
    find_product_name,
    find_product_parameters,
    find_product_price,
    find_product_quantity,
    find_product_rating,
    find_product_seller,
    is_buynow_offer
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
    def from_url(cls, url: str, proxies: List[str] = None, timeout: int = None):
        """
        ### Args
        - url: `str` a url of a product that we want to scrape
        - proxies: `List[str]` proxies list

        ### Returns
        - `Product` that contains the metadata of a product.
        """
        if "allegro.pl/oferta" not in url:
            if (
                "allegro.pl/events/clicks" not in url
                and "&redirect=https%3A%2F%2Fallegro.pl%2Foferta" not in url
            ):
                raise ValueError(f"Passed url is not that of a product: {url}")

        # try to parse product
        soup = get_soup(url=url, proxies=proxies, timeout=timeout)

        if is_buynow_offer(soup) is False:
            raise NotImplementedError("Auctions and advertisements are not supported")

        # Find name in parsed website
        name = find_product_name(soup)

        # Find price in parsed website
        price = find_product_price(soup)

        # Find category in parsed website
        category = find_product_category(soup)

        # Find seller in parsed website
        seller = find_product_seller(soup)

        # Find quantity in parsed website
        quantity = find_product_quantity(soup)

        # Find rating in parsed website
        rating = find_product_rating(soup)

        # Find images in parsed website
        images = find_product_images(soup)

        # Find parameters in parsed website
        parameters = find_product_parameters(soup)

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
