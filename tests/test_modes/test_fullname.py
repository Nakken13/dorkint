import pytest

from dorkint.builder import generate, refinements_of
from dorkint.modes import MODES

PRINCIPAL = "Jean Dupont"
FORBIDDEN = (
    "password", "passwd", "mot de passe", "secret", "token",
    "api_key", ".env", "credentials", "id_rsa", "dump",
)
EXPECTED_CATEGORIES = (
    "Social networks",
    "Named CVs and PDFs",
    "Academic work",
    "Public appearances",
    "Public records",
    "Portfolios",
    "Press",
)


def test_mode_registered() -> None:
    assert "fullname" in MODES
    assert set(refinements_of("fullname")) == {"city", "company"}


def test_expected_categories_present() -> None:
    names = set(MODES["fullname"].CATEGORIES)
    assert set(EXPECTED_CATEGORIES) <= names


def test_every_category_has_dork_with_quoted_principal() -> None:
    result = generate("fullname", PRINCIPAL)
    for category in MODES["fullname"].CATEGORIES:
        dorks = result.get(category)
        assert dorks, f"empty category: {category}"
        if category == "Name variants":
            continue  # built from first / last name, not the full quoted name
        assert all(f'"{PRINCIPAL}"' in d for d in dorks)


def test_key_sources_covered() -> None:
    queries = " ".join(d for ds in generate("fullname", PRINCIPAL).values() for d in ds)
    for source in (
        "linkedin.com", "facebook.com", "instagram.com", "twitter.com", "x.com", "github.com",
        "filetype:pdf", "theses.fr", "hal.science", "youtube.com",
        "journal-officiel.gouv.fr", "bodacc.fr", "data.gouv.fr",
    ):
        assert source in queries, source


def test_refinements_add_cross_dorks() -> None:
    base = generate("fullname", PRINCIPAL)
    ville = generate("fullname", PRINCIPAL, {"city": "Lyon"})
    both = generate("fullname", PRINCIPAL, {"city": "Lyon", "company": "Acme"})
    count = lambda r: sum(len(v) for v in r.values())
    assert count(base) < count(ville) < count(both)
    assert any('"Lyon"' in d for ds in ville.values() for d in ds)
    assert any('"Lyon"' in d and '"Acme"' in d for ds in both.values() for d in ds)


def test_company_only() -> None:
    result = generate("fullname", PRINCIPAL, {"company": "Acme"})
    assert any('"Acme"' in d for ds in result.values() for d in ds)
    assert not any('"Lyon"' in d for ds in result.values() for d in ds)


@pytest.mark.parametrize("term", FORBIDDEN)
def test_no_credentials_terms(term: str) -> None:
    for patterns in MODES["fullname"].CATEGORIES.values():
        for pattern in patterns:
            assert term not in pattern.lower()
