import logging
import requests

from bs4 import BeautifulSoup
from typing import Optional
from allegro.constants import HEADERS


def check_soup(
    url: str, proxies: dict = None, timeout: int = None
) -> Optional[BeautifulSoup]:
    try:
        # Send http GET request
        request = requests.get(url, headers=HEADERS, proxies=proxies, timeout=timeout)
    except Exception as e:
        logging.debug("Failed to get response from server")
        logging.debug(e)
        return None

    # Parse website
    soup = BeautifulSoup(request.text, "html.parser")

    if check_captcha(soup):
        return None
    else:
        return soup


def check_captcha(soup: BeautifulSoup) -> bool:
    # less than 10 divs so we probably got warning to enable javascript
    if len(soup.find_all("div")) < 10:
        return True

    return False
