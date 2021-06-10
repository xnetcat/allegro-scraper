from allegro.proxy import load_from_file, filter_proxies, scrape_free_proxy_lists

import pytest


@pytest.mark.vcr()
def test_free_proxies():
    """
    Test proxy gathering
    """
    proxies = scrape_free_proxy_lists()

    assert 50 == len(proxies)


def test_proxies_from_file(monkeypatch, tmpdir):
    monkeypatch.chdir(tmpdir)

    with open("proxies.txt", "w") as proxies:
        proxies.write(
            """159.8.114.37:8123
            169.57.1.85:8123
            176.98.75.229:54256
            119.81.71.27:8123
            119.81.189.194:8123
            95.165.182.230:45396
            103.25.170.72:9898
            159.8.114.34:8123
            159.65.69.186:9300
            169.57.1.84:80
            51.79.157.83:443
            119.81.189.194:80
            169.57.157.146:8123
            169.57.1.84:8123
            159.8.114.37:80
            119.81.71.27:80
            103.206.254.170:65103
            161.202.226.194:8123
            175.165.228.78:9999"""
        )

    proxies = load_from_file("proxies.txt")

    assert len(proxies) == 19


@pytest.mark.vcr()
def test_check_proxies():
    """
    Test proxy filtering
    """
    proxies = scrape_free_proxy_lists()

    proxies = filter_proxies(proxies, timeout=1)

    assert len(proxies) != 50
