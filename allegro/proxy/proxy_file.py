import logging

from typing import List
from pathlib import Path


def proxies_from_file(file_input: str) -> List[str]:
    file_object = Path(file_input)
    if file_object.exists():
        with open(file_object, "r") as file:
            content = file.read()
            proxies = content.split("\n")

            proxy_list = []

            if len(proxies) < 1:
                logging.error(f"Didn't find any proxies in {file_input}")

            for proxy in proxies:
                if proxy.count(".") == 3 and ":" in proxy:
                    proxy_list.append(proxy)
                else:
                    logging.warning(f'Wrong format for proxy "{proxy}"')

            return proxy_list
    else:
        logging.error(f"Wrong file, {file_input} does not exists")
        return []
