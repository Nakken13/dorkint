"""Tests du mode `ville` (France)."""

import pytest

from dorkint.builder import generer, get_mode

FORBIDDEN = (
    "password", "passwd", "mot de passe", "secret", "token",
    "api_key", ".env", "credentials", "id_rsa", "dump",
)


def test_mode_enregistre():
    mode = get_mode("city")
    assert mode.name == "city"
    assert "company" in mode.refinements


def test_chaque_categorie_produit_au_moins_un_dork():
    result = generer("city", "Nantes")
    for category in get_mode("city").categories:
        assert result.get(category.name), category.name


def test_valeur_principale_entre_guillemets():
    for dorks in generer("city", "Nantes").values():
        for dork in dorks:
            assert '"Nantes"' in dork.query


def test_affinage_entreprise_croise():
    base = generer("city", "Nantes")
    affine = generer("city", "Nantes", {"company": "Acme"})
    queries = [d.query for ds in affine.values() for d in ds]
    assert any('"Nantes"' in q and '"Acme"' in q for q in queries)
    assert sum(map(len, affine.values())) > sum(map(len, base.values()))
    assert not any('"Acme"' in d.query for ds in base.values() for d in ds)


def test_affinage_non_supporte_refuse():
    with pytest.raises(ValueError):
        generer("city", "Nantes", {"departement": "44"})


@pytest.mark.parametrize("affinages", [None, {"company": "Acme"}])
def test_aucun_terme_credentials(affinages):
    for dorks in generer("city", "Nantes", affinages).values():
        for dork in dorks:
            assert not any(t in dork.query.lower() for t in FORBIDDEN), dork.query


def test_sources_cles_presentes():
    queries = " ".join(d.query for ds in generer("city", "Nantes").values() for d in ds)
    for needle in ("data.gouv.fr", "societe.com", "pagesjaunes.fr", "filetype:pdf", "facebook.com/groups"):
        assert needle in queries
