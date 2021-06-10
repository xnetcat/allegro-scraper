from argparse import ArgumentParser


def _parse_basic(parser: ArgumentParser):
    # Search mode
    parser.add_argument("--search", "-s", type=str, nargs="+", help="search queries")

    # Crawl mode
    parser.add_argument("--crawl", "-c", type=str, nargs="+", help="Enables crawling")

    # Output file
    parser.add_argument(
        "--output", "-o", help="Output file ex. C:/test/file.json", required=True
    )

    opts, _ = parser.parse_known_args()
    if opts.search is None and opts.crawl is None:
        parser.error("--crawl/-c or --search/-s is required")

    return parser


def _parse_misc(parser: ArgumentParser):
    # Verbose mode
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        default=None,
        help="Will print more logging messages",
    )

    return parser


def _parse_filters(parser: ArgumentParser):
    # Sorting
    parser.add_argument(
        "--sorting",
        "-so",
        help="Sorting method",
        choices={
            "relevance_highest",
            "price_from_lowest",
            "price_from_highest",
            "price_with_delivery_from_lowest",
            "price_with_delivery_from_highest",
            "popularity_highest",
            "time_to_end_least",
            "time_added_latest",
        },
    )

    # Allegro Smart! free shipping
    parser.add_argument(
        "--smart-free-shipping",
        "-sfs",
        action="store_true",
        default=None,
        help="Allegro Smart! free shipping",
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
            "not_requiring_renovation",
        },
    )

    # Offer type
    parser.add_argument(
        "--offer-type",
        "-ot",
        nargs="+",
        type=str,
        help="Offer type",
        choices={"buy_now", "auction", "advertisement"},
    )

    # Minimal price
    parser.add_argument("--price-min", "-pmin", type=float, help="Minimal price")

    # Maximum price
    parser.add_argument("--price-max", "-pmax", type=float, help="Maximum price")

    # Delivery time
    parser.add_argument(
        "--delivery-time",
        "-dt",
        help="Delivery time",
        choices={"today", "one_day", "two_day"},
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
        },
    )

    # Delivery options
    parser.add_argument(
        "--delivery-options",
        "-do",
        nargs="+",
        type=str,
        help="Delivery options",
        choices={"free_shipping", "free_return"},
    )

    # City
    parser.add_argument("--city", "-ct", type=str, help="City")

    # Voivodeship
    parser.add_argument(
        "--voivodeship",
        "-vo",
        nargs="+",
        type=str,
        help="Voivodeship",
        choices={
            "dolnośląskie",
            "kujawsko_pomorskie",
            "lubelskie",
            "lubuskie",
            "łódzkie",
            "małopolskie",
            "mazowieckie",
            "opolskie",
            "podkarpackie",
            "podlaskie",
            "pomorskie",
            "śląskie",
            "świętokrzyskie",
            "warmińsko_mazurskie",
            "wielkopolskie",
            "zachodniopomorskie",
        },
    )

    # Product rating
    parser.add_argument(
        "--product-rating",
        "-pr",
        help="Product rating",
        choices={"from4.9", "from4.8", "from4.5"},
    )

    # Vat invoice
    parser.add_argument(
        "--vat-invoice", "-vat", action="store_true", default=None, help="Vat invoice"
    )

    # Allegro programs
    parser.add_argument(
        "--allegro-programs",
        "-ap",
        nargs="+",
        type=str,
        help="Allegro programs",
        choices={"allegro_coins", "brand_zone", "great_seller", "allegro_charity"},
    )

    # Occasions
    parser.add_argument(
        "--occasions",
        "-oc",
        nargs="+",
        type=str,
        help="Allegro programs",
        choices={"installments_of_zero_percent", "opportunity_zone", "great_price"},
    )

    return parser


def _parse_options(parser: ArgumentParser):
    # Max results
    parser.add_argument("--max-results", "-rmax", type=int, help="Max results")

    # Pages to fetch
    parser.add_argument("--pages-to-fetch", "-ptf", type=int, help="Pages to fetch")

    # Start page
    parser.add_argument("--start-page", "-sp", type=int, help="Start page")

    # Proxies file
    parser.add_argument(
        "--proxies-file", "-pf", type=str, help="Path to file with proxies"
    )

    # Use free proxies
    parser.add_argument(
        "--use-free-proxies",
        "-ufp",
        action="store_true",
        default=None,
        help="Use proxies from http://www.freeproxylists.net/",
    )

    # Check proxies
    parser.add_argument(
        "--check-proxies",
        "-cp",
        action="store_true",
        default=None,
        help="Check if proxies are not banned",
    )

    # Request timeout
    parser.add_argument("--request-timeout", "-rt", type=int, help="Request timeout")

    return parser


def parse_arguments():
    # Initialize argument parser
    parser = ArgumentParser(
        prog="allegro-spider",
        description="Allegro spider, product scrapper",
    )

    # Parse basic arguments
    parser = _parse_basic(parser)

    # Parse misc arguments
    parser = _parse_misc(parser)

    # Parse filter arguments
    parser = _parse_filters(parser)

    # Parse options arguments
    parser = _parse_options(parser)

    # Return parsed arguments
    return parser.parse_args()
