"""Tests du mode `tel` (numéro de téléphone FR)."""

import pytest

from dorkint.builder import generer, get_mode
from dorkint.modes.tel import variantes_tel

NUMERO = "06 12 34 56 78"
TERMES_INTERDITS = (
    "password", "passwd", "mot de passe", "secret", "token",
    "api_key", ".env", "credentials", "id_rsa", "dump",
)
CATEGORIES_ATTENDUES = {
    "Annuaires inversés": ("pagesjaunes.fr", "118712"),
    "Réseaux sociaux": ("facebook.com",),
    "Annonces": ("leboncoin.fr", "vinted.fr"),
    "Documents": ("filetype:pdf",),
    "Sites d'entreprise": ("contact",),
}


def test_mode_enregistre():
    assert get_mode("tel").name == "tel"


def test_chaque_categorie_produit_un_dork():
    result = generer("tel", NUMERO)
    for nom in [c.name for c in get_mode("tel").categories]:
        assert result[nom], nom
    for nom in (*CATEGORIES_ATTENDUES, "Mentions web"):
        assert nom in result


def test_principal_entre_guillemets():
    for dorks in generer("tel", NUMERO).values():
        for dork in dorks:
            assert f'"{NUMERO}"' in dork.query


def test_annuaires_et_annonces_ciblent_les_sites_fr():
    result = generer("tel", NUMERO)
    for categorie, marqueurs in CATEGORIES_ATTENDUES.items():
        texte = " ".join(d.query for d in result[categorie])
        for marqueur in marqueurs:
            assert marqueur in texte, (categorie, marqueur)


def test_affinages_croises():
    base = generer("tel", NUMERO)
    affine = generer("tel", NUMERO, {"ville": "Lyon", "entreprise": "Acme"})
    assert sum(map(len, affine.values())) > sum(map(len, base.values()))
    queries = [d.query for ds in affine.values() for d in ds]
    assert any('"Lyon"' in q for q in queries)
    assert any('"Acme"' in q for q in queries)
    assert any('"Lyon"' in q and '"Acme"' in q for q in queries)


def test_affinage_seul_n_injecte_pas_l_autre():
    queries = [d.query for ds in generer("tel", NUMERO, {"ville": "Lyon"}).values() for d in ds]
    assert any('"Lyon"' in q for q in queries)
    assert not any("{" in q for q in queries)


def test_aucun_terme_credentials():
    for template in (t for c in get_mode("tel").categories for t in c.templates):
        for terme in TERMES_INTERDITS:
            assert terme not in template.pattern.lower(), (template.pattern, terme)


@pytest.mark.parametrize("saisie", ["06 12 34 56 78", "06.12.34.56.78", "0612345678",
                                    "+33 6 12 34 56 78", "+33612345678", "0033612345678"])
def test_variantes_tel_normalise_toutes_les_saisies(saisie):
    assert variantes_tel(saisie) == [
        "06 12 34 56 78", "06.12.34.56.78", "0612345678",
        "+33 6 12 34 56 78", "+33612345678",
    ]


def test_variantes_tel_numero_non_francais_renvoie_la_saisie():
    assert variantes_tel("abc") == ["abc"]
    assert variantes_tel("+44 20 7946 0958") == ["+44 20 7946 0958"]


def test_toutes_les_ecritures_du_numero_sont_cherchees() -> None:
    requete = generer("tel", "06 12 34 56 78")["Mentions web"][0].query
    for ecriture in ("06 12 34 56 78", "06.12.34.56.78", "0612345678", "+33 6 12 34 56 78", "+33612345678"):
        assert f'"{ecriture}"' in requete
    assert " OR " in requete


def test_indicatif_avec_zero_entre_parentheses() -> None:
    assert variantes_tel("+33 (0)6 12 34 56 78") == variantes_tel("06 12 34 56 78")
