"""Tests of mode `phone` (FR phone number)."""

import pytest

from dorkint.builder import generate, get_mode
from dorkint.modes.phone import phone_variants

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
    assert get_mode("phone").name == "phone"


def test_chaque_categorie_produit_un_dork():
    result = generate("phone", NUMERO)
    for name in [c.name for c in get_mode("phone").categories]:
        assert result[name], name
    for name in (*CATEGORIES_ATTENDUES, "Mentions web"):
        assert name in result


def test_principal_entre_guillemets():
    for dorks in generate("phone", NUMERO).values():
        for dork in dorks:
            assert f'"{NUMERO}"' in dork.query


def test_annuaires_et_annonces_ciblent_les_sites_fr():
    result = generate("phone", NUMERO)
    for category, marqueurs in CATEGORIES_ATTENDUES.items():
        text = " ".join(d.query for d in result[category])
        for marqueur in marqueurs:
            assert marqueur in text, (category, marqueur)


def test_affinages_croises():
    base = generate("phone", NUMERO)
    affine = generate("phone", NUMERO, {"city": "Lyon", "company": "Acme"})
    assert sum(map(len, affine.values())) > sum(map(len, base.values()))
    queries = [d.query for ds in affine.values() for d in ds]
    assert any('"Lyon"' in q for q in queries)
    assert any('"Acme"' in q for q in queries)
    assert any('"Lyon"' in q and '"Acme"' in q for q in queries)


def test_affinage_seul_n_injecte_pas_l_autre():
    queries = [d.query for ds in generate("phone", NUMERO, {"city": "Lyon"}).values() for d in ds]
    assert any('"Lyon"' in q for q in queries)
    assert not any("{" in q for q in queries)


def test_aucun_terme_credentials():
    for template in (t for c in get_mode("phone").categories for t in c.templates):
        for terme in FORBIDDEN_TERMS:
            assert terme not in template.pattern.lower(), (template.pattern, terme)


@pytest.mark.parametrize("entry", ["06 12 34 56 78", "06.12.34.56.78", "0612345678",
                                    "+33 6 12 34 56 78", "+33612345678", "0033612345678"])
def test_variantes_tel_normalise_toutes_les_saisies(entry):
    assert phone_variants(entry) == [
        "06 12 34 56 78", "06.12.34.56.78", "0612345678",
        "+33 6 12 34 56 78", "+33612345678",
    ]


def test_variantes_tel_numero_non_francais_renvoie_la_saisie():
    assert phone_variants("abc") == ["abc"]
    assert phone_variants("+44 20 7946 0958") == ["+44 20 7946 0958"]


def test_toutes_les_ecritures_du_numero_sont_cherchees() -> None:
    query = generate("phone", "06 12 34 56 78")["Mentions web"][0].query
    for ecriture in ("06 12 34 56 78", "06.12.34.56.78", "0612345678", "+33 6 12 34 56 78", "+33612345678"):
        assert f'"{ecriture}"' in query
    assert " OR " in query


def test_indicatif_avec_zero_entre_parentheses() -> None:
    assert phone_variants("+33 (0)6 12 34 56 78") == phone_variants("06 12 34 56 78")
