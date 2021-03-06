import logging
import requests

from itertools import cycle

from bs4 import BeautifulSoup
from typing import Optional, List
from allegro.constants import HEADERS
from allegro.utils.check import check_captcha


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


def get_soup(url: str, proxies: List[str] = None, timeout: int = None):
    # Default values
    proxy_cycle = None
    current_proxy = None
    start_proxy = None
    proxy_object = None

    # Init proxy cycle
    if proxies is not None and len(proxies) >= 1:
        proxy_cycle = cycle(proxies)
        current_proxy = next(proxy_cycle)
        start_proxy = current_proxy
        if current_proxy is not None:
            proxy_object = {
                "https": f"https://{current_proxy}",
            }

    # try to get soup
    soup = check_soup(url, proxies=proxy_object, timeout=timeout)

    # captcha is required
    if soup is None:
        # Proxy failed so we change proxy
        if proxy_cycle is not None:
            current_proxy = next(proxy_cycle)
            logging.debug(f'Changing proxy to "{current_proxy}"')

        while True:
            if proxy_cycle is not None and current_proxy is not None:
                # We've run out of proxies to use
                if start_proxy == current_proxy:
                    raise OSError("We can't bypass IP block")

                # Update proxy object
                proxy_object = {
                    "https": f"https://{current_proxy}",
                }

                # Get soup
                soup = check_soup(url=url, proxies=proxy_object)

                # soup is fine return it
                if soup is not None:
                    return soup
                else:
                    # Soup is wrong, try again
                    current_proxy = next(proxy_cycle)
                    logging.debug(f'Changing proxy to "{current_proxy}"')
            else:
                raise OSError("You are being IP restricted, please use proxies")
    else:
        # soup is fine return it
        return soup
