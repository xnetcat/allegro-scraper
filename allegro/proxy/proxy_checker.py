import logging
import requests

from typing import List


def is_bad_proxy(proxy: str) -> bool:
    try:
        requests.get(
            url="https://google.com/",
            proxies={
                "https": f"https://{proxy}"
            },
            timeout=1
        )

        return True
    except:
        return False


def filter_proxies(proxies: List[str]) -> List[str]:
    good_proxies = []

    for index, proxy in enumerate(proxies):
        logging.info(f"Checking proxy [{index + 1}/{len(proxies)}]")
        is_good_proxy = not is_bad_proxy(proxy)

        if is_good_proxy is True:
            good_proxies.append(proxy)

    return proxies
