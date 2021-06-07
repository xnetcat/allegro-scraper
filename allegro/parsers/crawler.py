import requests

from bs4 import BeautifulSoup


def parse_website(url: str, proxies: dict = None):
    # Default headers
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0",  # noqa: E501
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
    }

    # Send http GET request
    request = requests.get(
        url,
        headers=headers,
        proxies=proxies,
    )

    # Parse html with BeautifulSoup
    soup = BeautifulSoup(request.text, "html.parser")

    # return soup
    return soup
