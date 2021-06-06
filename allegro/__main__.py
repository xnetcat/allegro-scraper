import argparse
import json
import logging

from dataclasses import asdict
from allegro.search.product import Product
from allegro.search import crawler


def parse_arguments():
    parser = argparse.ArgumentParser(
        prog="spotdl-spider",
        description="Allegro spider, product scrapper",
    )
    parser.add_argument("queries", type=str, nargs="+", help="search queries")
    parser.add_argument(
        "--output", "-o", help=r"Output file ex. C:/test/file.json", required=True
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        default=False,
        help="Will print more logging messages",
    )

    return parser.parse_args()


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
    for query in arguments.queries:
        # Single allegro offer
        if "allegro.pl/oferta/" in query:
            product = Product.from_url(query)
            products.append(product)
        else:
            # Search term (we get only first page of results)
            results = crawler.search(query)
            products.extend(results)

    # Convert products to dicts
    products = [asdict(var) for var in products if var is not None]

    # Dump dicts to json string
    json_dump = json.dumps(products, indent=4, ensure_ascii=False)

    # Save json to file
    with open(arguments.output, "w", encoding="utf-8") as output:
        logging.info(f"Saving to {arguments.output}")
        output.write(json_dump)


if __name__ == "__main__":
    console_entry_point()
