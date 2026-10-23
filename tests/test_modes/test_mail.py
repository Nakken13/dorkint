import re

import pytest

from dorkint.builder import generer, get_mode

ADRESSE = "jean@exemple.fr"
FORBIDDEN = re.compile(
    r"password|passwd|mot de passe|secret|token|api_key|\.env|credentials|id_rsa|dump|leak|combo",
    re.IGNORECASE,
)


def test_mode_enregistre() -> None:
    mode = get_mode("mail")
    assert mode.name == "mail"
    assert set(mode.refinements) == {"ville", "entreprise"}


def test_chaque_categorie_produit_un_dork() -> None:
    mode = get_mode("mail")
    result = generer("mail", ADRESSE)
    for category in mode.categories:
        assert result.get(category.name), f"catégorie vide : {category.name}"


def test_valeur_principale_entre_guillemets() -> None:
    for dorks in generer("mail", ADRESSE, {"ville": "Lyon", "entreprise": "Acme"}).values():
        for dork in dorks:
            assert f'"{ADRESSE}"' in dork.query or '"jean' in dork.query  # partie locale seule


def test_categories_attendues() -> None:
    names = " | ".join(generer("mail", ADRESSE)).lower()
    for expected in ("web", "pdf", "réseaux", "forum", "annuaire", "presse", "partie locale"):
        assert expected in names


def test_pdf_filetype() -> None:
    queries = [d.query for ds in generer("mail", ADRESSE).values() for d in ds]
    assert any("filetype:pdf" in q for q in queries)


def test_affinages_croises() -> None:
    base = generer("mail", ADRESSE)
    full = generer("mail", ADRESSE, {"ville": "Lyon", "entreprise": "Acme"})
    count = lambda r: sum(len(v) for v in r.values())
    assert count(full) > count(base)
    queries = [d.query for ds in full.values() for d in ds]
    assert any('"Lyon"' in q for q in queries)
    assert any('"Acme"' in q for q in queries)
    assert any('"Lyon"' in q and '"Acme"' in q for q in queries)
    ville_only = [d.query for ds in generer("mail", ADRESSE, {"ville": "Lyon"}).values() for d in ds]
    assert not any("Acme" in q for q in ville_only)


def test_aucun_terme_credentials() -> None:
    mode = get_mode("mail")
    for category in mode.categories:
        assert not FORBIDDEN.search(category.name)
        for template in category.templates:
            assert not FORBIDDEN.search(template.pattern), template.pattern


def test_pas_de_doublon() -> None:
    queries = [d.query for ds in generer("mail", ADRESSE, {"ville": "Lyon", "entreprise": "Acme"}).values() for d in ds]
    assert len(queries) == len(set(queries))


@pytest.mark.parametrize("affinage", ["nom", "pays"])
def test_affinage_inconnu_refuse(affinage: str) -> None:
    from dorkint.builder import DorkintError

    with pytest.raises(DorkintError):
        generer("mail", ADRESSE, {affinage: "x"})


def test_partie_locale_et_domaine_recherchees_separement() -> None:
    requetes = [d.query for d in generer("mail", "jean.dupont@exemple.fr")["Partie locale et domaine"]]
    assert '"jean.dupont"' in requetes
    assert '"jean.dupont" site:exemple.fr' in requetes
    assert '"jean.dupont" -site:exemple.fr' in requetes


def test_valeur_sans_arobase_n_a_pas_de_variantes_locale_domaine() -> None:
    requetes = [d.query for d in generer("mail", "jean.dupont")["Partie locale et domaine"]]
    assert all("site:exemple" not in q for q in requetes)
    assert '"jean.dupont"' not in requetes
