import pytest

from dorkint.builder import DorkintError, generate, refinements_of
from dorkint.modes import MODES

FORBIDDEN = (
    "password",
    "passwd",
    "mot de passe",
    "secret",
    "token",
    "api_key",
    ".env",
    "credentials",
    "id_rsa",
    "dump",
    "config sensible",
)


def test_mode_registered() -> None:
    assert "site" in MODES
    assert refinements_of("site") == ("company",)


def test_every_category_has_a_dork() -> None:
    result = generate("site", "exemple.fr")
    for category in MODES["site"].CATEGORIES:
        assert result.get(category), category


def test_expected_categories_present() -> None:
    names = set(MODES["site"].CATEGORIES)
    assert len(names) >= 8


def test_domain_is_raw_in_site_operator() -> None:
    result = generate("site", "exemple.fr")
    queries = [d for dorks in result.values() for d in dorks]
    assert "site:*.exemple.fr -www" in queries
    assert "site:exemple.fr" in " ".join(queries)
    assert 'site:"exemple.fr"' not in " ".join(queries)


def test_external_mentions_exclude_the_domain() -> None:
    queries = [d for dorks in generate("site", "exemple.fr").values() for d in dorks]
    assert any(q.startswith("-site:exemple.fr") and '"exemple.fr"' in q for q in queries)


def test_directory_listings_and_documents() -> None:
    joined = " ".join(d for dorks in generate("site", "exemple.fr").values() for d in dorks)
    assert 'intitle:"index of"' in joined
    assert "filetype:pdf" in joined


def test_refinement_entreprise_adds_dorks() -> None:
    base = sum(len(v) for v in generate("site", "exemple.fr").values())
    refined = generate("site", "exemple.fr", {"company": "Acme"})
    assert sum(len(v) for v in refined.values()) > base
    assert any('"Acme"' in d for dorks in refined.values() for d in dorks)


def test_unknown_refinement_rejected() -> None:
    with pytest.raises(DorkintError):
        generate("site", "exemple.fr", {"city": "Paris"})


@pytest.mark.parametrize("refinements", [{}, {"company": "Acme"}])
def test_no_credentials_terms_outside_the_site_scoped_exception(refinements: dict[str, str]) -> None:
    """Credentials terms are only tolerated when the query is anchored to the audited site
    (see `src/dorkint/guardrails.py` and DISCLAIMER.md § No credentials)."""
    for dorks in generate("site", "exemple.fr", refinements).values():
        for dork in dorks:
            lowered = dork.lower()
            if any(term in lowered for term in FORBIDDEN):
                assert dork.startswith("site:exemple.fr "), dork


def test_no_credentials_terms_in_templates_and_names_outside_the_site_scoped_exception() -> None:
    for category, patterns in MODES["site"].CATEGORIES.items():
        if any(term in category.lower() for term in FORBIDDEN):
            raise AssertionError(category)
        for pattern in patterns:
            if any(term in pattern.lower() for term in FORBIDDEN):
                assert pattern.startswith("site:{raw} "), pattern
