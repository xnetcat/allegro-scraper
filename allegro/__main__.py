from allegro.types.types_crawler import Parameters
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

    # Search querries
    parser.add_argument(
        "queries",
        type=str,
        nargs="+",
        help="search queries"
    )

    # Crawl mode
    parser.add_argument(
        "--crawl",
        "-c",
        action="store_true",
        help="Enables crawling"
    )

    # Sorting
    parser.add_argument(
        "--sorting",
        "-s",
        help="Sorting method",
        choices={
            "relevance_highest",
            "price_from_lowest",
            "price_from_highest",
            "price_with_delivery_from_lowest",
            "price_with_delivery_from_highest",
            "popularity_highest",
            "tome_to_end_least",
            "time_added_latest"
        }
    )

    # Allegro Smart! free shipping
    parser.add_argument(
        "--smart-free-shipping",
        "-sfs",
        action="store_true",
        help="Allegro Smart! free shipping"
    )

    # Product condition
    parser.add_argument(
        "--product-condition",
        "-pc",
        nargs="+",
        type=str,
        help="Product condition",
        choices={
            "new",
            "used",
            "incomplete_set",
            "new_without_tags",
            "new_with_defect",
            "after_return",
            "aftermarket",
            "regenerated",
            "damaged",
            "refurbished",
            "for_renovation",
            "not_requiring_renovation"
        }
    )

    # Offer type
    parser.add_argument(
        "--offer-type",
        "-ot",
        nargs="+",
        type=str,
        help="Offer type",
        choices={
            "buy_now",
            "auction",
            "advertisement"
        }
    )

    # Minimal price
    parser.add_argument(
        "--price-min",
        "-pmin",
        type=float,
        help="Minimal price"
    )

    # Maximum price
    parser.add_argument(
        "--price-max",
        "-pmax",
        type=float,
        help="Maximum price"
    )

    # Delivery time
    parser.add_argument(
        "--delivery-time",
        "-dt",
        help="Delivery time",
        choices={
            "today",
            "one_day",
            "two_day"
        }
    )

    # Delivery methods
    parser.add_argument(
        "--delivery-methods",
        "-dm",
        nargs="+",
        type=str,
        help="Delivery methods",
        choices={
            "courier",
            "inpost_parcel_locker",
            "overseas_delivery",
            "pickup_at_the_point",
            "letter",
            "package",
            "pickup",
            "email",
        }
    )

    # Delivery options
    parser.add_argument(
        "--delivery-options",
        "-do",
        nargs="+",
        type=str,
        help="Delivery options",
        choices={
            "free_shipping",
            "free_return"
        }
    )

    # Output file
    parser.add_argument(
        "--output",
        "-o",
        help=r"Output file ex. C:/test/file.json",
        required=True
    )

    # Verbose mode
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
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
            if arguments.crawl:
                # Parameters
                parameters: Parameters = {  # type: ignore
                    "sorting": arguments.sorting,
                    "smart_free_shipping": arguments.smart_free_shipping,
                    "product_condition": arguments.product_condition,
                    "offer_type": arguments.offer_type,
                    "price_min": arguments.price_min,
                    "price_max": arguments.price_max,
                    "delivery_time:": arguments.delivery_time,
                    "delivery_methods": arguments.delivery_methods,
                    "delivery_options": arguments.delivery_options
                }

                results = crawler.crawl(query, parameters=parameters)
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
