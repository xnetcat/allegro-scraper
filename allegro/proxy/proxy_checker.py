import logging
import requests

from typing import List
from bs4 import BeautifulSoup
from allegro.parsers.offer import is_captcha_required


def is_good_proxy(proxy: str, timeout: int = None) -> bool:
    try:
        # Default headers
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",  # noqa: E501
            "Referer": "https://allegro.pl",
            "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9,pl;q=0.8",
            "Sec-Fetch-Dest": "image",
            "Sec-Fetch-Mode": "no-cors",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Gpc": "1",
        }

        # Send http GET request
        request = requests.get(
            url="https://allegro.pl/oferta/typ-c-kabel-quick-charge-3-0-szybkie-ladowanie-7865547535",  # noqa: E501
            headers=headers,
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

        logging.info(
            f'Proxy "{proxy}" is' " "
            if proxy_is_working is True
            else " not " f"working [{index + 1}/{len(proxies)}]"
        )

    return good_proxies
