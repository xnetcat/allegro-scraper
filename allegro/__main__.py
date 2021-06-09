import json
import logging
import random

from dataclasses import asdict

import requests
from allegro.search import crawler
from allegro.types.filters import Filters
from allegro.types.options import Options
from allegro.search.product import Product
from allegro.parsers.arguments import parse_arguments
from allegro.proxy.proxy_checker import filter_proxies
from allegro.proxy.proxy_gatherer import scrape_free_proxy_lists


def console_entry_point():
    # Namespace containing parsed arguments
    arguments = parse_arguments()

    # Proxies list
    proxies = []

    # List containing Product objects
    products = []

    # Create filters dict
    filters: Filters = {  # type: ignore
        "sorting": arguments.sorting,
        "smart_free_shipping": arguments.smart_free_shipping,
        "product_condition": arguments.product_condition,
        "offer_type": arguments.offer_type,
        "price_min": arguments.price_min,
        "price_max": arguments.price_max,
        "delivery_time:": arguments.delivery_time,
        "delivery_methods": arguments.delivery_methods,
        "delivery_options": arguments.delivery_options,
        "city": arguments.city,
        "voivodeship": arguments.voivodeship,
        "product_rating": arguments.product_rating,
        "vat_invoice": arguments.vat_invoice,
        "allegro_programs": arguments.allegro_programs,
        "occasions": arguments.occasions,
    }

    # Create options dict
    options: Options = {  # type: ignore
        "include_sponsored_offers": arguments.include_sponsored_offers,  # not implemented yet
        "max_results": arguments.max_results,
        "pages_to_fetch": arguments.pages_to_fetch,
        "start_page": arguments.start_page,
        "avoid_duplicates": arguments.avoid_duplicates,
        "use_free_proxies": arguments.use_free_proxies,
        "check_proxies": arguments.check_proxies,
    }

    # Set up logging
    logging.basicConfig(
        level=logging.DEBUG if arguments.verbose else logging.INFO,
        format="%(asctime)s :: %(module)s :: [%(levelname)s] %(message)s"
        if arguments.verbose
        else "[%(levelname)s] %(message)s",
    )

    if options.get("use_free_proxies") is True:
        logging.info("Gathering proxies...")
        proxies = scrape_free_proxy_lists()
        logging.info(f"Finished gatgering proxies, found {len(proxies)} proxies")

    if options.get("check_proxies") is True and len(proxies) >= 1:
        logging.info(f"Checking {len(proxies)} proxies")
        proxies = filter_proxies(proxies)
        logging.info(f"Finished checking proxies, working proxies: {len(proxies)}")

    # Search for specified products
    if arguments.search is not None and len(arguments.search) >= 1:
        # Iterate over all search arguments
        for query in arguments.search:
            # Single allegro offer
            if "allegro.pl/oferta/" in query:
                # Create product object using url
                product = Product.from_url(
                    url=query,
                    proxy=random.choice(proxies),
                    timeout=options.get("request_timeout"),
                )

                # Add product to products list
                products.append(product)
            # Search term (we get only first page of results)
            else:
                # Start crawling
                results = crawler.search(query)

                # Extend product list with search results
                products.extend(results)

    # Crawl specified search terms
    if arguments.crawl is not None and len(arguments.crawl) >= 1:
        # Iterate over all crawl argumets
        for query in arguments.crawl:
            # Start crawling
            results = crawler.crawl(query, filters=filters, options=options)

            # Add results to products list
            products.extend(results)

    # Convert products to dicts
    products = [asdict(var) for var in products if var is not None]

    # Dump dicts to json string
    json_dump = json.dumps(products, indent=4, ensure_ascii=False)

    # Save json to file
    with open(arguments.output, "w", encoding="utf-8") as output:
        logging.info(f"Saving {len(products)} products to {arguments.output}")
        output.write(json_dump)


if __name__ == "__main__":
    console_entry_point()
