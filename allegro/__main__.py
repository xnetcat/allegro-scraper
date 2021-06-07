from allegro.types.types_crawler import Filters
import json
import logging

from dataclasses import asdict
from allegro.search.product import Product
from allegro.search import crawler
from allegro.parsers.arguments import parse_arguments


def console_entry_point():
    arguments = parse_arguments()

    # Set up logging
    logging.basicConfig(
        level=logging.DEBUG if arguments.verbose else logging.INFO,
        format="%(asctime)s :: %(module)s :: [%(levelname)s] %(message)s"
        if arguments.verbose
        else "[%(levelname)s] %(message)s",
    )

    # List containing Product objects
    products = []

    # Search for specified products
    if arguments.search is not None and len(arguments.search) >= 1:
        for query in arguments.search:
            # Single allegro offer
            if "allegro.pl/oferta/" in query:
                product = Product.from_url(query)
                products.append(product)
            else:
                # Search term (we get only first page of results)
                results = crawler.search(query)
                products.extend(results)

    # Crawl specified search terms
    if arguments.crawl is not None and len(arguments.crawl) >= 1:
        for query in arguments.crawl:
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
                "occasions": arguments.occasions
            }

            results = crawler.crawl(query, filters=filters)
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
