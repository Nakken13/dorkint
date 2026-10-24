"""Tests of mode `city` (France)."""

import pytest

from dorkint.builder import generate, refinements_of
from dorkint.modes import MODES

FORBIDDEN = (
    "password", "passwd", "mot de passe", "secret", "token",
    "api_key", ".env", "credentials", "id_rsa", "dump",
)


def test_mode_enregistre():
    assert "city" in MODES
    assert "company" in refinements_of("city")


def test_chaque_categorie_produit_au_moins_un_dork():
    result = generate("city", "Nantes")
    for category in MODES["city"].CATEGORIES:
        assert result.get(category), category


def test_primary_value_is_quoted():
    for dorks in generate("city", "Nantes").values():
        for dork in dorks:
            assert '"Nantes"' in dork


def test_affinage_entreprise_croise():
    base = generate("city", "Nantes")
    affine = generate("city", "Nantes", {"company": "Acme"})
    queries = [d for ds in affine.values() for d in ds]
    assert any('"Nantes"' in q and '"Acme"' in q for q in queries)
    assert sum(map(len, affine.values())) > sum(map(len, base.values()))
    assert not any('"Acme"' in d for ds in base.values() for d in ds)


def test_affinage_non_supporte_refuse():
    with pytest.raises(ValueError):
        generate("city", "Nantes", {"departement": "44"})


@pytest.mark.parametrize("refinements", [None, {"company": "Acme"}])
def test_aucun_terme_credentials(refinements):
    for dorks in generate("city", "Nantes", refinements).values():
        for dork in dorks:
            assert not any(t in dork.lower() for t in FORBIDDEN), dork


def test_sources_cles_presentes():
    queries = " ".join(d for ds in generate("city", "Nantes").values() for d in ds)
    for needle in ("data.gouv.fr", "societe.com", "pagesjaunes.fr", "filetype:pdf", "facebook.com/groups"):
        assert needle in queries
