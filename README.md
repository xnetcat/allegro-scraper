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

- #### To scrape one offer

  ```bash
  allegro-spider [offerUrl]
  ```

  example:

  ```bash
  allegro-spider https://allegro.pl/oferta/latarka-czolowa-petzl-actik-core-red-czolowka-450-10162449851
  ```

- #### To scrape multiple offers

  ```bash
  allegro-spider [offer1] [offer2] [offer3] ...
  ```

  example

  ```bash
  allegro-spider https://allegro.pl/oferta/zestaw-solarny-kolektor-sloneczny-2-0-eco-2-200-10727343060 https://allegro.pl/oferta/lodka-zanetowa-2-komorowa-7-4v-5200mah-hit-na-ryby-10545491921 https://allegro.pl/oferta/proszek-na-mrowki-likwiduje-gniazda-bros-trutka-9401994058
  ```

- #### To save data in a file

  ```bash
  allegro-spider [query] --output file.json
  ```

  example:

  ```bash
  allegro-spider [query] --output C:\\Users\\xnetcat\\Desktop\\allegro.json
  ```

- #### To crawl only first page of results

  ```bash
  allegro-spider [searchTerm]
  ```

  example:

  ```bash
  allegro-spider "rtx 3090"
  ```

- #### To crawl multiple search terms (only first page)

  ```bash
  allegro-spider [searchTerm1] [searchTerm2] [searchTerm3] ...
  ```

  example:

  ```bash
  allegro-spider "rtx 3090" "rtx 3080" "rtx 3070"
  ```
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
