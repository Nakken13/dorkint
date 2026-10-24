import re

import pytest

from dorkint.builder import generate, refinements_of
from dorkint.modes import MODES

ADRESSE = "jean@exemple.fr"
FORBIDDEN = re.compile(
    r"password|passwd|mot de passe|secret|token|api_key|\.env|credentials|id_rsa|dump|leak|combo",
    re.IGNORECASE,
)


def test_mode_enregistre() -> None:
    assert "email" in MODES
    assert set(refinements_of("email")) == {"city", "company"}


def test_chaque_categorie_produit_un_dork() -> None:
    result = generate("email", ADRESSE)
    for category in MODES["email"].CATEGORIES:
        assert result.get(category), f"empty category: {category}"


def test_primary_value_is_quoted() -> None:
    for category, dorks in generate("email", ADRESSE, {"city": "Lyon", "company": "Acme"}).items():
        for dork in dorks:
            if category == "Local part and domain" and "site:jean" not in dork and '"jean"' in dork:
                continue  # dorks on the local part only
            if category == "Obfuscated forms":
                continue  # anti-spam spellings of the address (jean at exemple dot fr)
            assert f'"{ADRESSE}"' in dork


def test_expected_categories() -> None:
    names = " | ".join(generate("email", ADRESSE)).lower()
    for expected in ("web", "pdf", "social", "forum", "directories", "press", "local part"):
        assert expected in names


def test_pdf_filetype() -> None:
    queries = [d for ds in generate("email", ADRESSE).values() for d in ds]
    assert any("filetype:pdf" in q for q in queries)


def test_affinages_croises() -> None:
    base = generate("email", ADRESSE)
    full = generate("email", ADRESSE, {"city": "Lyon", "company": "Acme"})
    count = lambda r: sum(len(v) for v in r.values())
    assert count(full) > count(base)
    queries = [d for ds in full.values() for d in ds]
    assert any('"Lyon"' in q for q in queries)
    assert any('"Acme"' in q for q in queries)
    assert any('"Lyon"' in q and '"Acme"' in q for q in queries)
    ville_only = [d for ds in generate("email", ADRESSE, {"city": "Lyon"}).values() for d in ds]
    assert not any("Acme" in q for q in ville_only)


def test_aucun_terme_credentials() -> None:
    for category, patterns in MODES["email"].CATEGORIES.items():
        assert not FORBIDDEN.search(category)
        for pattern in patterns:
            assert not FORBIDDEN.search(pattern), pattern


def test_pas_de_doublon() -> None:
    queries = [d for ds in generate("email", ADRESSE, {"city": "Lyon", "company": "Acme"}).values() for d in ds]
    assert len(queries) == len(set(queries))


@pytest.mark.parametrize("affinage", ["name", "pays"])
def test_unknown_refinement_is_rejected(affinage: str) -> None:
    from dorkint.builder import DorkintError

    with pytest.raises(DorkintError):
        generate("email", ADRESSE, {affinage: "x"})


def test_partie_locale_et_domaine_recherchees_separement() -> None:
    requetes = [d for d in generate("email", "jean.dupont@exemple.fr")["Local part and domain"]]
    assert '"jean.dupont" site:exemple.fr' in requetes
    assert '"jean.dupont" -site:exemple.fr' in requetes


def test_value_without_at_sign_has_no_local_domain_variants() -> None:
    requetes = [d for d in generate("email", "jean.dupont")["Local part and domain"]]
    assert all("site:exemple" not in q for q in requetes)
    assert not any("site:" in q and "jean.dupont" in q and "-site:linkedin" not in q for q in requetes)


@pytest.mark.parametrize("entry", ["jean@localhost", "a@b@c.fr", "jean@", "@exemple.fr", "jean@exemple.fr foo"])
def test_invalid_address_has_no_derived_values(entry: str) -> None:
    requetes = [d for d in generate("email", entry)["Local part and domain"]]
    assert not any("site:exemple" in q or "site:localhost" in q or "site:c.fr" in q for q in requetes)


def test_git_commit_dorks_target_code_hosts_with_the_quoted_address() -> None:
    dorks = generate("email", ADRESSE)["Git commits"]
    queries = [d for d in dorks]
    assert any("site:github.com" in q and "commit" in q for q in queries)
    assert any("site:gitlab.com" in q and "commit" in q for q in queries)
    assert any("Signed-off-by" in q for q in queries)
    assert all(f'"{ADRESSE}"' in q for q in queries)
