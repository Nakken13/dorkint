from urllib.parse import quote_plus

import dorkint


def test_package_importable() -> None:
    assert dorkint.__version__ == "0.1.0"


def test_url_encoding_of_a_dork() -> None:
    assert quote_plus('site:example.com "Jean Dupont"') == "site%3Aexample.com+%22Jean+Dupont%22"
