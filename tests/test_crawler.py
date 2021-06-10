import pytest

from allegro.types.options import Options
from allegro.search.crawler import search, crawl


@pytest.mark.vcr()
def test_search():
    products = search("kabel")

    assert len(products) >= 50


@pytest.mark.vcr()
def test_crawl_max_results():
    options: Options = {"max_results": 3}  # type: ignore

    products = crawl("kabel", options=options)

    assert len(products) == 3
