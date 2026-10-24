import pytest

from dorkint.builder import generate, refinements_of
from dorkint.modes import MODES

CATEGORIES = (
    "FR registers",
    "data.gouv.fr and Journal Officiel / BODACC",
    "Job offers",
    "Press and social networks",
    "Subdomains and exposed files",
    "Executives and officers",
)
FORBIDDEN = ("password", "passwd", "mot de passe", "secret", "token", "api_key", ".env", "credentials", "id_rsa", "dump")


def _all_queries(result: dict) -> list[str]:
    return [d for dorks in result.values() for d in dorks]


def test_mode_registered() -> None:
    assert "company" in MODES
    assert "city" in refinements_of("company")


def test_every_category_has_dork() -> None:
    result = generate("company", "Acme")
    assert tuple(result) == CATEGORIES
    assert all(result[c] for c in CATEGORIES)


def test_principal_quoted_everywhere() -> None:
    assert all('"Acme"' in q for q in _all_queries(generate("company", "Acme")))


def test_siren_principal() -> None:
    assert all('"552100554"' in q for q in _all_queries(generate("company", "552100554")))


@pytest.mark.parametrize(
    "site",
    [
        "site:infogreffe.fr", "site:societe.com", "site:pagesjaunes.fr", "site:pappers.fr",
        "site:annuaire-entreprises.data.gouv.fr", "site:bodacc.fr", "site:journal-officiel.gouv.fr",
        "site:welcometothejungle.com", "site:indeed.fr", "site:linkedin.com/jobs", "site:apec.fr",
        "filetype:pdf",
    ],
)
def test_expected_sources(site: str) -> None:
    assert any(site in q for q in _all_queries(generate("company", "Acme")))


def test_city_refinement_crosses() -> None:
    base = _all_queries(generate("company", "Acme"))
    crossed = _all_queries(generate("company", "Acme", {"city": "Lyon"}))
    assert len(crossed) > len(base)
    assert any('"Acme"' in q and '"Lyon"' in q for q in crossed)
    assert not any("Lyon" in q for q in base)


def test_no_credentials_terms() -> None:
    queries = _all_queries(generate("company", "Acme", {"city": "Lyon"}))
    for q in queries:
        assert not any(term in q.lower() for term in FORBIDDEN), q
