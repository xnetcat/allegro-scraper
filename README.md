<div align="center">

# allegro-spider

Allegro scraping tool

[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?style=flat-square&color=44CC11)](https://github.com/xnetcat/allegro-spider/blob/master/LICENSE)

</div>

> The fastest, easiest most accurate allegro crawler/spider/product scrapper

## Installation

### Installing allegro-spider

- Recommended Stable Version:

  ```bash
  pip install allegro-spider
  ```

- Dev Version: **(NOT STABLE)**

  ```bash
  pip install https://codeload.github.com/xnetcat/allegro-spider/zip/dev
  ```

## Usage

<details>
    <summary style="font-size:1.25em">
        <strong>Basic usage</strong>
    </summary>

- #### To scrape one offer

  ```bash
  allegro-spider -s [offerUrl]
  ```

  example:

  ```bash
  allegro-spider -s https://allegro.pl/oferta/latarka-czolowa-petzl-actik-core-red-czolowka-450-10162449851
  ```

- #### To scrape multiple offers

  ```bash
  allegro-spider -s [offer1] [offer2] [offer3] ...
  ```

  example

  ```bash
  allegro-spider -s https://allegro.pl/oferta/zestaw-solarny-kolektor-sloneczny-2-0-eco-2-200-10727343060 https://allegro.pl/oferta/lodka-zanetowa-2-komorowa-7-4v-5200mah-hit-na-ryby-10545491921 https://allegro.pl/oferta/proszek-na-mrowki-likwiduje-gniazda-bros-trutka-9401994058
  ```

- #### To scrape only first page of results for search term

  ```bash
  allegro-spider -s [searchTerm]
  ```

  example:

  ```bash
  allegro-spider -s "rtx 3090"
  ```

- #### To scrape multiple search terms (only first page)

  ```bash
  allegro-spider -s [searchTerm1] [searchTerm2] [searchTerm3] ...
  ```

  example:

  ```bash
  allegro-spider -s "rtx 3090" "rtx 3080" "rtx 3070"
  ```

- #### To crawl a search term

  ```bash
  allegro-spider -c [searchTerm]
  ```

  example:

  ```bash
  allegro-spider -c "rtx 2070"
  ```

  > _Note: crawling without specifying filters or options defaults to scraping first page_

- #### To crawl multiple search terms

  ```bash
  allegro-spider -c [searchTerm1] [searchTerm2] [searchTerm3] ...
  ```

  example:

  ```bash
  allegro-spider -c "rtx 2060" "rtx 2070" "rtx 2080"
  ```

  > _Note: crawling without specifying filters or options defaults to scraping first page_

- #### To save data in a file

  ```bash
  allegro-spider -s/-c [args] --output file.json
  ```

  example:

  ```bash
  allegro-spider -s/-c [args] --output C:\\Users\\xnetcat\\Desktop\\allegro.json
  ```
</details>

<details>
    <summary style="font-size:1.25em">
        <strong>Crawling filters</strong>
    </summary>

</details>

<details>
    <summary style="font-size:1.25em">
        <strong>Crawling options</strong>
    </summary>

</details>

## `pipx` Isolated Environment Alternative

For users who are not familiar with `pipx`, it can be used to run scripts **without**
installing the allegro-spider package and all the dependencies globally with pip.

First, you will need to install `pipx` by running:

```bash
python3 -m pip install --user pipx
python3 -m pipx ensurepath
```

Next, you can jump directly to running allegro-spider with:

```bash
pipx run allegro-spider ...
```

## Authors

[@xnetcat](https://github.com/xnetcat)

## License

[MIT](/LICENSE)
