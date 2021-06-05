import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(
        prog="spotdl-spider",
        description="Allegro spider, product scrapper",
    )
    parser.add_argument("queries", type=str, nargs="+", help="search queries")

    return parser.parse_args()


def console_entry_point():
    arguments = parse_arguments()

    for query in arguments.queries:
        print(query)


if __name__ == "__main__":
    console_entry_point()
