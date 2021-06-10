from itertools import product
import json

import pytest

from dataclasses import asdict
from allegro.search.product import Product

@pytest.mark.vcr()
def test_scrape_from_url():
    """
    Test create product from url
    """
    product = Product.from_url(
        "https://allegro.pl/oferta/5-x-test-antygenowy-domowy-dokladnosc-96-79-10572320477"
        )

    assert product.name == "5 x TEST ANTYGENOWY DOMOWY DOKŁADNOŚĆ 96,79"
    assert product.category == "https://allegro.pl/kategoria/zdrowie-medycyna-testy-diagnostyczne-122577"
    assert product.price == 57.98
    assert product.seller == "Simon-Trade"
    assert product.quantity >= 5000
    assert product.rating >= 4.0
    assert len(product.images) == 2
    assert len(product.parameters.keys()) >= 3


def test_product_from_dump():
    """
    Test create product from dump
    """
    product_dump = {
        "url": "https://allegro.pl/oferta/typ-c-kabel-quick-charge-3-0-szybkie-ladowanie-7865547535",
        "name": "TYP-C KABEL QUICK CHARGE 3.0 SZYBKIE ŁADOWANIE",
        "category": "https://allegro.pl/kategoria/kable-pojedyncze-kable-4793",
        "price": 5.9,
        "seller": "NELASTYL",
        "quantity": 8314,
        "rating": 4.84,
        "images": [
            "https://a.allegroimg.com/s128/11a5c1/3a3c17b34b6da7949ba7a1a977b0/TYP-C-KABEL-QUICK-CHARGE-3-0-SZYBKIE-LADOWANIE",
            "https://a.allegroimg.com/s128/119390/45d4e29344f195833ee8a04e05b5/TYP-C-KABEL-QUICK-CHARGE-3-0-SZYBKIE-LADOWANIE-Kod-producenta-KB3",
            "https://a.allegroimg.com/s128/116ade/40829ca64d52862c313c0931a78c/TYP-C-KABEL-QUICK-CHARGE-3-0-SZYBKIE-LADOWANIE-Kolor-czarny",
            "https://a.allegroimg.com/s128/114ddb/6a5fbf024b038b6c0eac9b452bde/TYP-C-KABEL-QUICK-CHARGE-3-0-SZYBKIE-LADOWANIE-Producent-Nela-Styl",
            "https://a.allegroimg.com/s128/1154a4/5a69a8564463b358f9d337c145fa/TYP-C-KABEL-QUICK-CHARGE-3-0-SZYBKIE-LADOWANIE-Dlugosc-przewodu-1-m",
            "https://a.allegroimg.com/s128/116d64/dacf999345a7a189f74627a58f1d/TYP-C-KABEL-QUICK-CHARGE-3-0-SZYBKIE-LADOWANIE-Konstrukcja-oplot",
            "https://a.allegroimg.com/s128/11b2b7/7bcd50b048c1b87089c82a42c282/TYP-C-KABEL-QUICK-CHARGE-3-0-SZYBKIE-LADOWANIE-Zlacza-USB-USB-typ-C",
            "https://a.allegroimg.com/s128/110b09/73f165354d0a845d42be97b2a11a/TYP-C-KABEL-QUICK-CHARGE-3-0-SZYBKIE-LADOWANIE-EAN-5903686014031",
            "https://a.allegroimg.com/s128/11af46/aaa2004440369759ef8c8840529d",
            "https://a.allegroimg.com/s128/118997/38649e464405b43653f3e4131dc6",
            "https://seller-extras.allegrostatic.com/seller-extras-5e/logotype_9323196_ba8ae74f-e5a3-4fec-951b-a8e0c80389e3"
        ],
        "parameters": {
            "Stan": "Nowy",
            "Faktura": "Wystawiam fakturę VAT",
            "Kod producenta": "KB3",
            "Kolor": "czarny",
            "Producent": "Nela-Styl",
            "Długość przewodu": "1 m",
            "Konstrukcja": "oplot",
            "Złącza": "USB - USB typ C"
        }
    }

    product = Product.from_data_dump(json.dumps(product_dump))

    assert asdict(product) == product_dump

def test_wrong_product():
    """
    Tests wrong url passed to from_url function
    """
    with pytest.raises(ValueError, match=r"Passed url is not that of a product: https://allegro.pl/") as excinfo:
        Product.from_url("https://allegro.pl/")
