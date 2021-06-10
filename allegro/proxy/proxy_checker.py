import logging
import requests

from typing import List
from bs4 import BeautifulSoup
from allegro.constants import HEADERS
from allegro.parsers.offer import is_captcha_required


def is_good_proxy(proxy: str, timeout: int = None) -> bool:
    try:
        # Send http GET request
        request = requests.get(
            url="https://allegro.pl/oferta/typ-c-kabel-quick-charge-3-0-szybkie-ladowanie-7865547535",  # noqa: E501
            headers=HEADERS,
            timeout=timeout,
            proxies={"http": f"https://{proxy}", "https": f"https://{proxy}"},
        )

        # Parse website
        soup = BeautifulSoup(request.text, "html.parser")

        if is_captcha_required(soup):
            logging.debug("Captcha is required")
            return False
        else:
            return True
    except Exception as e:
        logging.debug("Can't connect to proxy server")
        logging.debug(e)
        return False


def filter_proxies(proxies: List[str], timeout: int = None) -> List[str]:
    good_proxies = []

    for index, proxy in enumerate(proxies):
        proxy_is_working = is_good_proxy(proxy, timeout)

        if proxy_is_working is True:
            good_proxies.append(proxy)

        message = (
            f'Proxy "{proxy}" is'
            f' {"" if proxy_is_working is True else "not "}working'
            f" [{index + 1}/{len(proxies)}]"
        )

        logging.info(message)

    return good_proxies
