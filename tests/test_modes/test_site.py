import pytest

from dorkint.builder import DorkintError, generer, get_mode

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
    mode = get_mode("site")
    assert mode.name == "site"
    assert mode.refinements == ("company",)


def test_every_category_has_a_dork() -> None:
    mode = get_mode("site")
    result = generer("site", "exemple.fr")
    for category in mode.categories:
        assert result.get(category.name), category.name


def test_expected_categories_present() -> None:
    names = {c.name for c in get_mode("site").categories}
    assert len(names) >= 8


def test_domain_is_raw_in_site_operator() -> None:
    result = generer("site", "exemple.fr")
    queries = [d.query for dorks in result.values() for d in dorks]
    assert "site:*.exemple.fr -www" in queries
    assert "site:exemple.fr" in " ".join(queries)
    assert 'site:"exemple.fr"' not in " ".join(queries)


def test_external_mentions_exclude_the_domain() -> None:
    queries = [d.query for dorks in generer("site", "exemple.fr").values() for d in dorks]
    assert any(q.startswith("-site:exemple.fr") and '"exemple.fr"' in q for q in queries)


def test_directory_listings_and_documents() -> None:
    joined = " ".join(d.query for dorks in generer("site", "exemple.fr").values() for d in dorks)
    assert 'intitle:"index of"' in joined
    assert "filetype:pdf" in joined


def test_refinement_entreprise_adds_dorks() -> None:
    base = sum(len(v) for v in generer("site", "exemple.fr").values())
    refined = generer("site", "exemple.fr", {"company": "Acme"})
    assert sum(len(v) for v in refined.values()) > base
    assert any('"Acme"' in d.query for dorks in refined.values() for d in dorks)


def test_unknown_refinement_rejected() -> None:
    with pytest.raises(DorkintError):
        generer("site", "exemple.fr", {"city": "Paris"})


@pytest.mark.parametrize("affinages", [{}, {"company": "Acme"}])
def test_no_credentials_terms(affinages: dict[str, str]) -> None:
    for dorks in generer("site", "exemple.fr", affinages).values():
        for dork in dorks:
            lowered = dork.query.lower()
            assert not any(term in lowered for term in FORBIDDEN), dork.query


def test_no_credentials_terms_in_templates_and_names() -> None:
    for category in get_mode("site").categories:
        for text in (category.name, *(t.pattern for t in category.templates)):
            assert not any(term in text.lower() for term in FORBIDDEN), text
