import argparse
import json

from dataclasses import asdict
from allegro.search.product import Product
from allegro.search.crawl import crawl

def parse_arguments():
    parser = argparse.ArgumentParser(
        prog="spotdl-spider",
        description="Allegro spider, product scrapper",
    )
    parser.add_argument("queries", type=str, nargs="+", help="search queries")
    parser.add_argument("--output", "-o", help=r"Output file ex. C:/test/file.json", required=True)

    return parser.parse_args()


def console_entry_point():
    arguments = parse_arguments()
    products = []

    for query in arguments.queries:
        if "allegro.pl/oferta/" in query:
            product = Product.from_url(query)
            products.append(product)
        else:
            results = crawl(query)
            products.extend(results)

    new_list = []
    for product in products:
        new_list.append(asdict(product))

    json_dump = json.dumps(new_list, indent=4, ensure_ascii=False)

    with open(arguments.output, "w", encoding="utf-8") as output:
        output.write(json_dump)

if __name__ == "__main__":
    console_entry_point()
