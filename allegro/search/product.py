from dataclasses import dataclass, asdict
from typing import List
import json

import requests
import bs4

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
    rating: int
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
            raise Exception(f"Passed url is not that of a product: {url}")

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache'
        }

        request = requests.get(url, proxies=proxy, headers=headers)
        soup = bs4.BeautifulSoup(request.text, "html.parser")

        buy_now_button = soup.find("button", attrs={"type": "submit", "id": "buy-now-button", "data-analytics-interaction-custom-flow-type": "BuyNow"})
        if buy_now_button is None:
            raise NotImplementedError("Auctions and offers are not supported")

        name = soup.find("meta", attrs={"property": "og:title"}).get('content')
        price = float(soup.find("meta", attrs={"itemprop": "price"}).get('content'))
        category = [div for div in soup.find_all("div", attrs={"data-role": "breadcrumb-item", "itemscope": True, "itemprop":"itemListElement", "itemtype": "http://schema.org/ListItem"}) if "allegro.pl/kategoria" in div.find("a").get("href")][-1].find("a").get("href")
        seller = soup.find("div", attrs={"data-analytics-interaction-label": "sellerInfo", "data-analytics-interaction-custom-url": "#aboutSeller"}).find("div").text
        quantity = int(soup.find("input", attrs={"type": "number", "name": "quantity"}).get("max"))
        rating = float(soup.find("meta", attrs={"itemprop": "ratingValue"}).get('content'))
        images = [img.find("img").get("src") for img in soup.find_all("div", attrs={"role": "button", "tabindex": "0"}) if img.find("img") is not None]

        # this part could probably be optimized but idk how
        parameters = {}
        parameters_div = soup.find("div", attrs={"data-box-name": "Parameters", "data-prototype-id": "allegro.showoffer.parameters", "data-analytics-category": "allegro.showoffer.parameters"})
        parameters_list = parameters_div.find("ul", attrs={"data-reactroot": True})
        segments = parameters_list.find_all("li", recursive=False)
        for segment in segments:
            # idk how to name variables
            parts_holder = segment.find("div")
            parts = parts_holder.find_all("div")
            for part in parts:
                parameter_objects = part.find_all("li")
                for parameter_object in parameter_objects:
                    data_container = parameter_object.find("div")
                    objects = data_container.find_all("div")
                    key = objects[0].text
                    value = objects[1].text

                    parameters[key] = value

        return cls(
            url,
            name,
            category,
            price,
            seller,
            quantity,
            rating,
            images,
            parameters
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
