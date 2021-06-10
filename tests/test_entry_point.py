import logging
import sys

import pytest

from allegro.__main__ import console_entry_point
from allegro.search import crawler
from allegro.search.product import Product


@pytest.fixture()
def patch_dependencies(mocker):
    """This is a helper fixture to patch out everything that shouldn't be called here"""
    mocker.patch.object(crawler, "crawl", autospec=True)
    mocker.patch.object(crawler, "search", autospec=True)
    mocker.patch.object(Product, "from_url", autospec=True)


def test_no_search_or_crawl(capsys, monkeypatch):
    """
    This will fail because there is no options
    """
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "dummy",
            "-o",
            "typ-c-kabel-quick-charge-3-0-szybkie-ladowanie-7865547535.json",
        ],
    )

    with pytest.raises(SystemExit):
        console_entry_point()

    out, err = capsys.readouterr()

    assert "allegro-spider: error: --crawl/-c or --search/-s is required\n" in err


@pytest.mark.vcr()
def test_scrape_single_product(caplog, monkeypatch):
    """
    This will scrape single product
    """
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "dummy",
            "-s"
            "https://allegro.pl/oferta/typ-c-kabel-quick-charge-3-0-szybkie-ladowanie-7865547535",
            "-o",
            "typ-c-kabel-quick-charge-3-0-szybkie-ladowanie-7865547535.json",
        ],
    )

    caplog.set_level(logging.INFO)

    console_entry_point()

    assert (
        "root",
        logging.INFO,
        "Saving 1 products to typ-c-kabel-quick-charge-3-0-szybkie-ladowanie-7865547535.json",
    ) in caplog.record_tuples


@pytest.mark.vcr()
def test_scrape_first_page(caplog, monkeypatch):
    """
    This will search first page
    """
    monkeypatch.setattr(
        sys,
        "argv",
        ["dummy", "-s" "kabel usb", "-o", "kable.json"],
    )

    caplog.set_level(logging.INFO)

    console_entry_point()

    assert (
        "root",
        logging.INFO,
        "Saving 0 products to kable.json",
    ) not in caplog.record_tuples


@pytest.mark.vcr()
def test_crawl(caplog, monkeypatch):
    """
    This will try to fetch 20 pages but will stop on 5 results
    """
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "dummy",
            "-c",
            "kabel",
            "--max-results",
            "5",
            "--pages-to-fetch",
            "20",
            "--output",
            "crawl.json",
        ],
    )

    caplog.set_level(logging.INFO)

    console_entry_point()

    assert (
        "root",
        logging.INFO,
        "Saving 5 products to crawl.json",
    ) in caplog.record_tuples


@pytest.mark.vcr()
def test_wrong_search(caplog, monkeypatch):
    """
    This will try to search for products but will fail
    """
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "dummy",
            "-s",
            "sadvnasdvjkasvdkjbasvdabsdvjkabsj",
            "-o" "does_not_exist.json",
        ],
    )

    caplog.set_level(logging.INFO)

    console_entry_point()

    assert (
        "root",
        logging.INFO,
        "Saving 0 products to does_not_exist.json",
    ) in caplog.record_tuples
