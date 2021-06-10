import logging
import requests

from itertools import cycle
from bs4 import BeautifulSoup
from typing import List, Optional


# It's the same as parse_website but we can't use parse_website
def parse_product(url: str, proxies: List[str] = None, timeout: int = None):
    # Init proxy cycle
    if proxies is not None and len(proxies) >= 1:
        proxy_cycle = cycle(proxies)
        current_proxy = next(proxy_cycle)
        start_proxy = current_proxy
        proxy_object = {
            "http": f"https://{current_proxy}",
            "https": f"https://{current_proxy}"
        }
    else:
        proxy_cycle = None
        current_proxy = None
        start_proxy = None
        proxy_object = None

    # try to get soup
    soup = get_soup_check(url, proxies=proxy_object, timeout=timeout)

    # captcha is required
    if soup is None:
        # Proxy failed so we change proxy
        if proxy_cycle is not None:
            current_proxy = next(proxy_cycle)
            logging.debug(f"Changing proxy to \"{current_proxy}\"")

        while True:
            if proxy_cycle is not None and current_proxy is not None:
                # We've run out of proxies to use
                if start_proxy == current_proxy:
                    raise OSError("We can't bypass IP block")

                # Update proxy object
                proxy_object = {"http": f"https://{current_proxy}", "https": f"https://{current_proxy}"}

                # Get soup
                soup = get_soup_check(url=url, proxies=proxy_object)

                # soup is fine return it
                if soup is not None:
                    return soup
                else:
                    # Soup is wrong, try again
                    current_proxy = next(proxy_cycle)
                    logging.debug(f"Changing proxy to \"{current_proxy}\"")
            else:
                raise OSError("You are being IP restricted, please use proxies")
    else:
        # soup is fine return it
        return soup


def get_soup_check(url: str, proxies: dict = None, timeout: int = None) -> Optional[BeautifulSoup]:
    # Default headers
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36", # noqa: E501
        "Referer": "https://allegro.pl",
        "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9,pl;q=0.8",
        "Sec-Fetch-Dest": "image",
        "Sec-Fetch-Mode": "no-cors",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Gpc": "1"
    }

    try:
        # Send http GET request
        request = requests.get(
            url,
            headers=headers,
            proxies=proxies,
            timeout=timeout
        )
    except:
        return None

    # Parse website
    soup = BeautifulSoup(request.text, "html.parser")

    if is_captcha_required(soup):
        return None
    else:
        return soup


def is_captcha_required(soup: BeautifulSoup) -> bool:
    # less than 10 divs so we probably got warning to enable javascript
    if len(soup.find_all("div")) < 10:
        return True

    return False


def _is_buynow_offer(soup: BeautifulSoup) -> bool:
    buy_now_button = soup.find(
        "button",
        attrs={
            "type": "submit",
            "id": "buy-now-button",
            "data-analytics-interaction-custom-flow-type": "BuyNow",
        },
    )

    return buy_now_button is not None


def _find_product_name(soup: BeautifulSoup) -> str:
    product_name = soup.find("meta", attrs={"property": "og:title"}).get("content")

    return product_name


def _find_product_category(soup: BeautifulSoup) -> str:
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


def _find_product_price(soup: BeautifulSoup) -> float:
    product_price = float(soup.find("meta", attrs={"itemprop": "price"}).get("content"))

    return product_price


def _find_product_seller(soup: BeautifulSoup) -> str:
    seller = soup.find(
        "a",
        attrs={"href": "#aboutSeller", "data-analytics-click-value": "sellerLogin"},
    ).text.split(" - ")[0]

    return seller


def _find_product_quantity(soup: BeautifulSoup) -> int:
    quantity = soup.find("input", attrs={"type": "number", "name": "quantity"}).get(
        "max"
    )

    return int(quantity)


def _find_product_rating(soup: BeautifulSoup) -> float:
    rating_object = soup.find("meta", attrs={"itemprop": "ratingValue"})
    if rating_object is not None:
        rating = rating_object.get("content")
    else:
        rating = 0

    return float(rating)


def _find_product_images(soup: BeautifulSoup) -> List[str]:
    images = [
        img.find("img").get("src")
        for img in soup.find_all("div", attrs={"role": "button", "tabindex": "0"})
        if img.find("img") is not None
    ]

    return images


def _find_product_parameters(soup: BeautifulSoup) -> dict:
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
