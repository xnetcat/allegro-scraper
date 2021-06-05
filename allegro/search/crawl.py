import requests
import bs4

from allegro.search.product import Product
from typing import List

def crawl(search_term: str, proxies=None) -> List[Product]:
    products = []
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

    req = requests.get(f"https://allegro.pl/listing?string={search_term}", headers=headers, proxies=proxies)
    soup = bs4.BeautifulSoup(req.text, "html.parser")

    sections = soup.find_all("article", attrs={"data-role": "offer", "data-analytics-view-custom-index0": True, "data-analytics-view-custom-deliverylabel": True, "data-analytics-view-custom-page": True, "data-analytics-view-value": True})
    print("FOUND ", len(sections), " products")
    for section in sections:
        product_a = section.find("a", attrs={"rel": "nofollow", "tabindex": "-1"})

        product = Product.from_url(product_a.get("href"))

        print("Found: ", product.name)

        products.append(product)

    return products
