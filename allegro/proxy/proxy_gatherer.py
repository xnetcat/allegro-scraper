import re
import requests

from bs4 import BeautifulSoup
from urllib.parse import unquote


def scrape_free_proxy_lists():
    # HTTP Headers
    headers = {
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",  # noqa: E501
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",  # noqa: E501
        "Referer": "http://www.freeproxylists.net/",
        "Accept-Language": "en,ru-RU;q=0.9,ru;q=0.8,en-US;q=0.7,uk;q=0.6",
    }

    # HTTP Params
    params = (
        ("c", ""),
        ("pt", ""),
        ("pr", "HTTPS"),
        ("a[]", ["0", "1", "2"]),
        ("u", "0"),
    )

    try:
        # Send request
        response = requests.get(
            "http://www.freeproxylists.net/",
            headers=headers,
            params=params,
            verify=False,
        )

        # Parse website
        soup = BeautifulSoup(response.content, "html5lib")

        # Init proxies list
        proxies = []

        # Iterate over table
        for tr in soup.select_one(".DataGrid tbody").find_all("tr")[1:]:
            # Find proxies info
            tds = [x.find(text=True) for x in tr.find_all("td")]

            # ignore wrong results
            if len(tds) == 1:
                continue

            # Find ip
            ip = re.search(
                r">(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})<", unquote(tds[0])
            ).group(1)

            # Find port
            port = tds[1]

            # Add proxy to list
            proxies.append("%s:%s" % (ip, port))
    except:
        # Return empty array if we've failed
        return []

    # Return proxies list
    return proxies
