"""Operator crossings: every mode combines advanced operators and stays well-formed."""

import re

import pytest

from dorkint.builder import generate
from dorkint.modes import MODES

SAMPLES = {
    "fullname": "Jean Dupont",
    "username": "jdupont",
    "email": "jean@exemple.fr",
    "phone": "06 12 34 56 78",
    "site": "exemple.fr",
    "company": "Acme",
}
REFINEMENTS = {"city": "Lyon", "company": "Acme"}
OPERATOR = re.compile(r"(?<![\w-])-?(\w+):")


def _queries(mode: str) -> list[str]:
    allowed = {"city": "Lyon"} if mode == "company" else REFINEMENTS
    if mode == "site":
        allowed = {"company": "Acme"}
    return [d for ds in generate(mode, SAMPLES[mode], allowed).values() for d in ds]


@pytest.mark.parametrize("mode", SAMPLES)
def test_mode_has_operator_crossings(mode: str) -> None:
    assert "Operator crossings" in generate(mode, SAMPLES[mode])


@pytest.mark.parametrize("mode", SAMPLES)
def test_quotes_and_parentheses_are_balanced(mode: str) -> None:
    for query in _queries(mode):
        assert query.count('"') % 2 == 0, query
        assert query.count("(") == query.count(")"), query


@pytest.mark.parametrize("mode", SAMPLES)
def test_allin_operators_are_not_mixed_with_other_operators(mode: str) -> None:
    """`allintext:`/`allintitle:`/`allinurl:` swallow the rest of the query: no other operator after them."""
    for query in _queries(mode):
        if match := re.search(r"allin(?:text|title|url):", query):
            assert not OPERATOR.search(query[match.end():]), query


@pytest.mark.parametrize("mode", SAMPLES)
def test_no_duplicates_with_refinements(mode: str) -> None:
    queries = _queries(mode)
    assert len(queries) == len(set(queries))


def test_every_advanced_operator_is_used_somewhere() -> None:
    queries = " ".join(q for mode in SAMPLES for q in _queries(mode))
    for operator in (
        "allintext:", "allintitle:", "allinurl:", "inanchor:", "intext:", "intitle:", "inurl:",
        "ext:", "after:", "before:", "AROUND(", "site:*.", " * ", " OR ", " -site:",
    ):
        assert operator in queries, operator


def test_fullname_name_variants() -> None:
    variants = generate("fullname", "Jean Dupont")["Name variants"]
    assert '"Jean * Dupont"' in variants
    assert '"Dupont, Jean"' in variants
    assert '"Jean" AROUND(3) "Dupont"' in variants
    assert "inurl:jean-dupont" in variants
    assert "inurl:jean.dupont" in variants


def test_fullname_slug_drops_accents() -> None:
    variants = generate("fullname", "Hélène Müller")["Name variants"]
    assert "inurl:helene-muller" in variants


def test_single_word_fullname_has_no_name_variants() -> None:
    assert "Name variants" not in generate("fullname", "Dupont")


def test_non_latin_name_has_no_url_slug() -> None:
    variants = generate("fullname", "李 王").get("Name variants", [])
    assert not any(v.startswith("inurl:") for v in variants)


def test_email_obfuscated_spellings() -> None:
    forms = generate("email", "jean@exemple.fr")["Obfuscated forms"]
    assert any('"jean at exemple dot fr"' in f and '"jean [at] exemple.fr"' in f for f in forms)
    assert '"jean" AROUND(5) exemple.fr' in forms


def test_email_without_address_has_no_obfuscated_forms() -> None:
    assert "Obfuscated forms" not in generate("email", "jean.dupont")


def test_dead_operators_are_not_used() -> None:
    """Operators removed from Google would always return nothing ([-])."""
    dead = re.compile(r"(?<![\w-])(?:cache|related|info|link|map|phonebook):", re.IGNORECASE)
    for mode in MODES:
        for category, patterns in MODES[mode].CATEGORIES.items():
            for pattern in patterns:
                assert not dead.search(pattern), (mode, category, pattern)
