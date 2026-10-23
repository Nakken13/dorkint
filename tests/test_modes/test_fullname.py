import pytest

from dorkint.builder import generer, get_mode

PRINCIPAL = "Jean Dupont"
FORBIDDEN = (
    "password", "passwd", "mot de passe", "secret", "token",
    "api_key", ".env", "credentials", "id_rsa", "dump",
)
EXPECTED_CATEGORIES = (
    "Réseaux sociaux",
    "CV et PDF nominatifs",
    "Travaux académiques",
    "Interventions publiques",
    "Actes publics",
    "Portfolios",
    "Presse",
)


def test_mode_registered() -> None:
    mode = get_mode("fullname")
    assert mode.name == "fullname"
    assert set(mode.refinements) == {"city", "company"}


def test_expected_categories_present() -> None:
    names = {c.name for c in get_mode("fullname").categories}
    assert set(EXPECTED_CATEGORIES) <= names


def test_every_category_has_dork_with_quoted_principal() -> None:
    result = generer("fullname", PRINCIPAL)
    for category in get_mode("fullname").categories:
        dorks = result.get(category.name)
        assert dorks, f"catégorie vide : {category.name}"
        assert all(f'"{PRINCIPAL}"' in d.query for d in dorks)


def test_key_sources_covered() -> None:
    queries = " ".join(d.query for ds in generer("fullname", PRINCIPAL).values() for d in ds)
    for source in (
        "linkedin.com", "facebook.com", "instagram.com", "twitter.com", "x.com", "github.com",
        "filetype:pdf", "theses.fr", "hal.science", "youtube.com",
        "journal-officiel.gouv.fr", "bodacc.fr", "data.gouv.fr",
    ):
        assert source in queries, source


def test_refinements_add_cross_dorks() -> None:
    base = generer("fullname", PRINCIPAL)
    ville = generer("fullname", PRINCIPAL, {"city": "Lyon"})
    both = generer("fullname", PRINCIPAL, {"city": "Lyon", "company": "Acme"})
    count = lambda r: sum(len(v) for v in r.values())
    assert count(base) < count(ville) < count(both)
    assert any('"Lyon"' in d.query for ds in ville.values() for d in ds)
    assert any('"Lyon"' in d.query and '"Acme"' in d.query for ds in both.values() for d in ds)


def test_company_only() -> None:
    result = generer("fullname", PRINCIPAL, {"company": "Acme"})
    assert any('"Acme"' in d.query for ds in result.values() for d in ds)
    assert not any('"Lyon"' in d.query for ds in result.values() for d in ds)


@pytest.mark.parametrize("term", FORBIDDEN)
def test_no_credentials_terms(term: str) -> None:
    for category in get_mode("fullname").categories:
        for template in category.templates:
            assert term not in template.pattern.lower()
