import logging

from typing import List
from allegro.search.product import Product


def is_good_proxy(proxy: str) -> bool:
    try:
        Product.from_url(
            url="https://allegro.pl/oferta/typ-c-kabel-quick-charge-3-0-szybkie-ladowanie-7865547535",
            proxy=proxy,
        )
    except:
        return False

    return True


def filter_proxies(proxies: List[str]) -> List[str]:
    good_proxies = []

    for index, proxy in enumerate(proxies):
        proxy_is_working = is_good_proxy(proxy)

        if proxy_is_working is True:
            good_proxies.append(proxy)

        logging.info(
            f"Proxy \"{proxy}\" is{' ' if proxy_is_working is True else ' not '}working [{index + 1}/{len(proxies)}]"
        )

    return good_proxies
