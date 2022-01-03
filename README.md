<div align="center">

# allegro-scraper

Allegro scraping tool

[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?style=flat-square&color=44CC11)](https://github.com/xnetcat/allegro-scraper/blob/master/LICENSE)

</div>

## It probably no longer works, example usage in `allegro/console/__init__.py`


## Installation

### Installing allegro-scraper

- Recommended Stable Version:

  ```bash
  pip install https://codeload.github.com/xnetcat/allegro-scraper/zip/main
  ```

- Dev Version: **(NOT STABLE)**

  ```bash
  pip install https://codeload.github.com/xnetcat/allegro-scraper/zip/dev
  ```

- Installing using zip file

  Download and unzip the archive and then cd into the folder and then run

  ```bash
  python setup.py install
  ```

## Usage

<details>
    <summary style="font-size:1.25em">
        <strong>Basic usage</strong>
    </summary>

- #### To scrape one offer

  ```bash
  allegro-scraper -s [offerUrl]
  ```

  example:

  ```bash
  allegro-scraper -s https://allegro.pl/oferta/latarka-czolowa-petzl-actik-core-red-czolowka-450-10162449851
  ```

- #### To scrape multiple offers

  ```bash
  allegro-scraper -s [offer1] [offer2] [offer3] ...
  ```

  example

  ```bash
  allegro-scraper -s https://allegro.pl/oferta/zestaw-solarny-kolektor-sloneczny-2-0-eco-2-200-10727343060 https://allegro.pl/oferta/lodka-zanetowa-2-komorowa-7-4v-5200mah-hit-na-ryby-10545491921 https://allegro.pl/oferta/proszek-na-mrowki-likwiduje-gniazda-bros-trutka-9401994058
  ```

- #### To scrape only first page of results for search term

  ```bash
  allegro-scraper -s [searchTerm]
  ```

  example:

  ```bash
  allegro-scraper -s "rtx 3090"
  ```

- #### To scrape multiple search terms (only first page)

  ```bash
  allegro-scraper -s [searchTerm1] [searchTerm2] [searchTerm3] ...
  ```

  example:

  ```bash
  allegro-scraper -s "rtx 3090" "rtx 3080" "rtx 3070"
  ```

- #### To crawl a search term

  ```bash
  allegro-scraper -c [searchTerm]
  ```

  example:

  ```bash
  allegro-scraper -c "rtx 2070"
  ```

  > _Note: crawling without specifying filters or options defaults to scraping first page_

- #### To crawl multiple search terms

  ```bash
  allegro-scraper -c [searchTerm1] [searchTerm2] [searchTerm3] ...
  ```

  example:

  ```bash
  allegro-scraper -c "rtx 2060" "rtx 2070" "rtx 2080"
  ```

  > _Note: crawling without specifying filters or options defaults to scraping first page_

- #### To save data in a file

  ```bash
  allegro-scraper -s/-c [args] --output file.json
  ```

  example:

  ```bash
  allegro-scraper -s/-c [args] --output C:\\Users\\xnetcat\\Desktop\\allegro.json
  ```
</details>

<details>
    <summary style="font-size:1.25em">
        <strong>Crawling filters</strong>
    </summary>

- #### Sorting

  ```bash
  --sorting/-so [sorting]
  ```

  type: `choice`

  choices:

  ```python
  "relevance_highest"
  "price_from_lowest"
  "price_from_highest"
  "price_with_delivery_from_lowest"
  "price_with_delivery_from_highest"
  "popularity_highest"
  "time_to_end_least"
  "time_added_latest"
  ```

  example:

  ```bash
  allegro-scraper -c "rtx 3090" --sorting time_added_latest
  ```

- #### Allegro Smart! free shipping

  ```bash
  --smart-free-shipping/-sfs
  ```

  type: `boolean`

  example:

  ```bash
  allegro-scraper -c "rtx 3090" --smart-free-shipping
  ```

- #### Product condition

  ```bash
  --product-condition/-pc [conditions]
  ```

  type: `list`

  choices:

  ```python
  "new"
  "used"
  "incomplete_set"
  "new_without_tags"
  "new_with_defect"
  "after_return"
  "aftermarket"
  "regenerated"
  "damaged"
  "refurbished"
  "for_renovation"
  "not_requiring_renovation"
  ```

  example:

  ```bash
  allegro-scraper -c "rtx 3090" -pc new used damaged
  ```

- #### Offer type

  ```bash
  --offer-type/-ot [types]
  ```

  type: `list`

  choices:

  ```python
  "buy_now"
  "auction"
  "advertisement"
  ```

  example:

  ```bash
  allegro-scraper -c "rtx 3090" -ot buy_now auction
  ```

- #### Minimal price

  ```bash
  --price-min/-pmin [price]
  ```

  type: `float`

  example:

  ```bash
  allegro-scraper -c "rtx 3090" -pmin 5000.25
  ```

- #### Maximum price

  ```bash
  --price-max/-pmax [price]
  ```

  type: `float`

  example:

  ```bash
  allegro-scraper -c "rtx 3090" -pmax 15000.00
  ```

- #### Delivery time

  ```bash
  --delivery-time/-dt [time]
  ```

  type: `choice
  `

  choices:

  ```python
  "today"
  "one_day"
  "two_day"
  ```

  example:

  ```bash
  allegro-scraper -c "rtx 3090" -dt today
  ```

- #### Delivery methods

  ```bash
  --delivery-methods/-dm [methods]
  ```

  type: `list`

  choices:

  ```python
  "courier"
  "inpost_parcel_locker"
  "overseas_delivery"
  "pickup_at_the_point"
  "letter"
  "package"
  "pickup"
  "email"
  ```

  example:

  ```bash
  allegro-scraper -c "rtx 3090" -dm email pickup package
  ```

- #### Delivery options

  ```bash
  --delivery-options/-do [options]
  ```

  type: `list`

  choices:

  ```python
  "free_shipping",
  "free_return"
  ```

  example:

  ```bash
  allegro-scraper -c "rtx 3090" -do free_shipping free_return
  ```

- #### City

  ```bash
  --city/-ct [city]
  ```

  type: `string`

  example:

  ```bash
  allegro-scraper -c "rtx 3090" -ct warszawa
  ```

- #### Voivodeship

  ```bash
  --voivodeship/-vo [voivodeship]
  ```

  type: `choice`

  choices:

  ```python
  "dolnośląskie"
  "kujawsko_pomorskie"
  "lubelskie"
  "lubuskie"
  "łódzkie"
  "małopolskie"
  "mazowieckie"
  "opolskie"
  "podkarpackie"
  "podlaskie"
  "pomorskie"
  "śląskie"
  "świętokrzyskie"
  "warmińsko_mazurskie"
  "wielkopolskie"
  "zachodniopomorskie"
  ```

  example:

  ```bash
  allegro-scraper -c "rtx 3090" -vo lubuskie
  ```

- #### Product rating

  ```bash
  --product-rating/-pr [rating]
  ```

  type: `choice`

  choices:

  ```python
  "from4.9"
  "from4.8"
  "from4.5"
  ```

  example:

  ```bash
  allegro-scraper -c "rtx 3090" -pr "from4.5"
  ```

- #### Vat invoice

  ```bash
  --vat-invoice/-vat
  ```

  type: `boolean`

  example:

  ```bash
  allegro-scraper -c "rtx 3090" --vat-invoice
  ```

- #### Allegro programs

  ```bash
  --allegro-programs/-ap [programs]
  ```

  type: `list`

  choices:

  ```python
  "allegro_coins"
  "brand_zone"
  "great_seller"
  "allegro_charity"
  ```

  example:

  ```bash
  allegro-scraper -c "rtx 3090" -ap great_seller allegro_charity
  ```

- #### Occasions

  ```bash
  --occasions/-oc [occasions]
  ```

  type: `list`

  choices:

  ```python
  "installments_of_zero_percent"
  "opportunity_zone"
  "great_price"
  ```

  example:

  ```bash
  allegro-scraper -c "rtx 3090" -oc great_price opportunity_zone
  ```

</details>

<details>
    <summary style="font-size:1.25em">
        <strong>Crawling options</strong>
    </summary>

- #### Max results

  ```bash
  --max-results/-rmax [results]
  ```

  type: `int`

  example:

  ```bash
  allegro-scraper -c "rtx 3090" -rmax 100
  ```

- #### Pages to fetch

  ```bash
  --pages-to-fetch/-ptf [pages]
  ```

  type: `int`

  example:

  ```bash
  allegro-scraper -c "rtx 3090" -ptf 5
  ```

- #### Start page

  ```bash
  --start-page/-sp [page]
  ```

  type: `int`

  example:

  ```bash
  allegro-scraper -c "rtx 3090" -sp 1
  ```

- #### Proxies file

  ```bash
  --proxies-file/-pf [file]
  ```

  type: `string`

  example:

  ```bash
  allegro-scraper -c "rtx 3090" -pf "C:/test/proxies.ttx"
  ```

- #### Use free proxies

  ```bash
  --use-free-proxies/-ufp
  ```

  type: `bool`

  example:

  ```bash
  allegro-scraper -c "rtx 3090" -ufp
  ```

- #### Check proxies

  ```bash
  --check-proxies/-cp
  ```

  type: `bool`

  example:

  ```bash
  allegro-scraper -c "rtx 3090" --use-free-proxies -cp
  ```

- #### Threads

  ```bash
  --threads/-t [threads]
  ```

  type: `int`

  example:

  ```bash
  allegro-scraper -c "rtx 3090" --thread 4
  ```

</details>

## Authors

[@xnetcat](https://github.com/xnetcat)

## License

[MIT](/LICENSE)
