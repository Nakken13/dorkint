"""Tests of mode `phone` (FR phone number)."""

import pytest

from dorkint.builder import generate
from dorkint.modes import MODES
from dorkint.modes.phone import values

NUMERO = "06 12 34 56 78"
FORBIDDEN_TERMS = (
    "password", "passwd", "mot de passe", "secret", "token",
    "api_key", ".env", "credentials", "id_rsa", "dump",
)
CATEGORIES_ATTENDUES = {
    "Reverse directories": ("pagesjaunes.fr", "118712"),
    "Social networks": ("facebook.com",),
    "Classifieds": ("leboncoin.fr", "vinted.fr"),
    "Documents": ("filetype:pdf",),
    "Company sites": ("contact",),
}


def test_mode_enregistre():
    assert "phone" in MODES


def test_chaque_categorie_produit_un_dork():
    result = generate("phone", NUMERO)
    for name in MODES["phone"].CATEGORIES:
        assert result[name], name
    for name in (*CATEGORIES_ATTENDUES, "Mentions web"):
        assert name in result


def test_principal_entre_guillemets():
    for dorks in generate("phone", NUMERO).values():
        for dork in dorks:
            assert f'"{NUMERO}"' in dork


def test_annuaires_et_annonces_ciblent_les_sites_fr():
    result = generate("phone", NUMERO)
    for category, marqueurs in CATEGORIES_ATTENDUES.items():
        text = " ".join(d for d in result[category])
        for marqueur in marqueurs:
            assert marqueur in text, (category, marqueur)


def test_affinages_croises():
    base = generate("phone", NUMERO)
    affine = generate("phone", NUMERO, {"city": "Lyon", "company": "Acme"})
    assert sum(map(len, affine.values())) > sum(map(len, base.values()))
    queries = [d for ds in affine.values() for d in ds]
    assert any('"Lyon"' in q for q in queries)
    assert any('"Acme"' in q for q in queries)
    assert any('"Lyon"' in q and '"Acme"' in q for q in queries)


def test_affinage_seul_n_injecte_pas_l_autre():
    queries = [d for ds in generate("phone", NUMERO, {"city": "Lyon"}).values() for d in ds]
    assert any('"Lyon"' in q for q in queries)
    assert not any("{" in q for q in queries)


def test_aucun_terme_credentials():
    for pattern in (p for patterns in MODES["phone"].CATEGORIES.values() for p in patterns):
        for terme in FORBIDDEN_TERMS:
            assert terme not in pattern.lower(), (pattern, terme)


@pytest.mark.parametrize("entry", ["06 12 34 56 78", "06.12.34.56.78", "0612345678",
                                    "+33 6 12 34 56 78", "+33612345678", "0033612345678"])
def test_variantes_tel_normalise_toutes_les_saisies(entry):
    assert values(entry) == values("06 12 34 56 78")
    assert values(entry)["primary"] == (
        '("06 12 34 56 78" OR "06.12.34.56.78" OR "0612345678" OR "+33 6 12 34 56 78" OR "+33612345678")'
    )


def test_variantes_tel_numero_non_francais_renvoie_la_saisie():
    assert values("abc") == {}
    assert values("+44 20 7946 0958") == {}


def test_toutes_les_ecritures_du_numero_sont_cherchees() -> None:
    query = generate("phone", "06 12 34 56 78")["Mentions web"][0]
    for ecriture in ("06 12 34 56 78", "06.12.34.56.78", "0612345678", "+33 6 12 34 56 78", "+33612345678"):
        assert f'"{ecriture}"' in query
    assert " OR " in query


def test_indicatif_avec_zero_entre_parentheses() -> None:
    assert values("+33 (0)6 12 34 56 78") == values("06 12 34 56 78")
