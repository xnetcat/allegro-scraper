# Running tests

## Installing dependencies

All the required dependencies can be installed via `pip`, by using the following command:

```shell
pip install -e .[test]
```

## Executing tests

After installing all the required modules, just call the following command from the root
directory:

```shell
pytest
```

To see code coverage use:

```shell
pytest --cov=allegro
```

## Enable network communication

To speed up the test execution, the network requests are mocked. That means that each HTTP
request does not reach the server, and the response is faked by the
[vcrpy](https://vcrpy.readthedocs.io/en/latest/index.html) module.

To run tests with a real network communication use this command:

```shell
pytest --disable-vcr
```

Whenever the server response will change and affect the tests behavior, the stored
responses can be updated by wiping the [tests/cassetes](tests/cassetes) directory and
running `pytest` again (without `--disable-vcr`).
