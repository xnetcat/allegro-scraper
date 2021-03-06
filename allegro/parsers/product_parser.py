from bs4 import BeautifulSoup
from typing import List


def is_buynow_offer(soup: BeautifulSoup) -> bool:
    buy_now_button = soup.find(
        "button",
        attrs={
            "type": "submit",
            "id": "buy-now-button",
            "data-analytics-interaction-custom-flow-type": "BuyNow",
        },
    )

    return buy_now_button is not None


def find_product_name(soup: BeautifulSoup) -> str:
    product_name = soup.find("meta", attrs={"property": "og:title"}).get("content")

    return product_name


def find_product_category(soup: BeautifulSoup) -> str:
    categories = [
        div
        for div in soup.find_all(
            "div",
            attrs={
                "data-role": "breadcrumb-item",
                "itemscope": True,
                "itemprop": "itemListElement",
                "itemtype": "http://schema.org/ListItem",
            },
        )
        if "allegro.pl/kategoria" in div.find("a").get("href")
    ]

    return categories[-1].find("a").get("href")


def find_product_price(soup: BeautifulSoup) -> float:
    product_price = float(soup.find("meta", attrs={"itemprop": "price"}).get("content"))

    return product_price


def find_product_seller(soup: BeautifulSoup) -> str:
    seller = soup.find(
        "a",
        attrs={"href": "#aboutSeller", "data-analytics-click-value": "sellerLogin"},
    ).text.split(" - ")[0]

    return seller


def find_product_quantity(soup: BeautifulSoup) -> int:
    quantity = soup.find("input", attrs={"type": "number", "name": "quantity"}).get(
        "max"
    )

    return int(quantity)


def find_product_rating(soup: BeautifulSoup) -> float:
    rating_object = soup.find("meta", attrs={"itemprop": "ratingValue"})
    if rating_object is not None:
        rating = rating_object.get("content")
    else:
        rating = 0

    return float(rating)


def find_product_images(soup: BeautifulSoup) -> List[str]:
    images = [
        img.find("img").get("src")
        for img in soup.find_all("div", attrs={"role": "button", "tabindex": "0"})
        if img.find("img") is not None
    ]

    return images


def find_product_parameters(soup: BeautifulSoup) -> dict:
    parameters = {}
    parameters_div = soup.find(
        "div",
        attrs={
            "data-box-name": "Parameters",
            "data-prototype-id": "allegro.showoffer.parameters",
            "data-analytics-category": "allegro.showoffer.parameters",
        },
    )

    parameters_list = parameters_div.find("ul", attrs={"data-reactroot": True})
    segments = parameters_list.find_all("li", recursive=False)
    for segment in segments:
        parts_holder = segment.find("div")
        parts = parts_holder.find_all("div")
        for part in parts:
            parameter_objects = part.find_all("li")
            for parameter_object in parameter_objects:
                data_container = parameter_object.find("div")
                objects = data_container.find_all("div")

                key = objects[0].text[:-1]
                value = objects[1].text

                parameters[key] = value

    return parameters
