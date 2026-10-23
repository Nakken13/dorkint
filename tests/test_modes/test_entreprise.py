import pytest

from dorkint.builder import generer, get_mode

CATEGORIES = (
    "Registres FR",
    "data.gouv.fr et Journal Officiel / BODACC",
    "Offres d'emploi",
    "Presse et réseaux sociaux",
    "Sous-domaines et fichiers exposés",
    "Dirigeants et mandataires",
)
FORBIDDEN = ("password", "passwd", "mot de passe", "secret", "token", "api_key", ".env", "credentials", "id_rsa", "dump")


def _all_queries(result: dict) -> list[str]:
    return [d.query for dorks in result.values() for d in dorks]


def test_mode_registered() -> None:
    assert get_mode("entreprise").name == "entreprise"
    assert "ville" in get_mode("entreprise").refinements


def test_every_category_has_dork() -> None:
    result = generer("entreprise", "Acme")
    assert tuple(result) == CATEGORIES
    assert all(result[c] for c in CATEGORIES)


def test_principal_quoted_everywhere() -> None:
    assert all('"Acme"' in q for q in _all_queries(generer("entreprise", "Acme")))


def test_siren_principal() -> None:
    assert all('"552100554"' in q for q in _all_queries(generer("entreprise", "552100554")))


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
    assert any(site in q for q in _all_queries(generer("entreprise", "Acme")))


def test_ville_refinement_crosses() -> None:
    base = _all_queries(generer("entreprise", "Acme"))
    crossed = _all_queries(generer("entreprise", "Acme", {"ville": "Lyon"}))
    assert len(crossed) > len(base)
    assert any('"Acme"' in q and '"Lyon"' in q for q in crossed)
    assert not any("Lyon" in q for q in base)


def test_no_credentials_terms() -> None:
    queries = _all_queries(generer("entreprise", "Acme", {"ville": "Lyon"}))
    for q in queries:
        assert not any(term in q.lower() for term in FORBIDDEN), q
