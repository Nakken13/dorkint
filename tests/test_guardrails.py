import pytest

from dorkint import builder
from dorkint.builder import Category, DorkintError, Mode, Template, generer
from dorkint.guardrails import TERMES_INTERDITS, termes_interdits


@pytest.mark.parametrize("terme", TERMES_INTERDITS)
def test_each_forbidden_term_is_detected(terme: str) -> None:
    assert termes_interdits(f'site:exemple.fr "{terme}"') == [terme]
    assert termes_interdits(f"intitle:{terme.upper()}") == [terme]


@pytest.mark.parametrize(
    "texte", ['site:exemple.fr "Jean Dupont"', "secrétariat mairie", "filetype:pdf cv", "tokenisation"]
)
def test_healthy_text_passes(texte: str) -> None:
    assert termes_interdits(texte) == []


def test_register_rejects_forbidden_template(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(builder, "_REGISTRY", {})
    mauvais = Mode("mauvais", (), (Category("X", (Template('filetype:env DB_PASSWORD {principal}'),)),))
    with pytest.raises(DorkintError, match="interdit"):
        builder.register(mauvais)
    assert "mauvais" not in builder._REGISTRY


def test_register_rejects_forbidden_category_name(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(builder, "_REGISTRY", {})
    mauvais = Mode("mauvais", (), (Category("Mots de passe", (Template("{principal}"),)),))
    with pytest.raises(DorkintError, match="interdit"):
        builder.register(mauvais)


def test_register_accepts_healthy_mode(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(builder, "_REGISTRY", {})
    builder.register(Mode("sain", (), (Category("X", (Template("{principal}"),)),)))


def test_every_registered_mode_is_clean() -> None:
    builder.load_modes()
    assert builder._REGISTRY, "aucun mode chargé"
    for mode in builder._REGISTRY.values():
        for categorie in mode.categories:
            assert termes_interdits(categorie.name) == [], (mode.name, categorie.name)
            for template in categorie.templates:
                assert termes_interdits(template.pattern) == [], (mode.name, template.pattern)


def test_every_generated_query_is_clean() -> None:
    builder.load_modes()
    for nom, mode in builder._REGISTRY.items():
        valeur = "exemple.fr" if nom == "site" else "Jean Dupont"
        affinages = {r: "Lyon" for r in mode.refinements}
        for dorks in generer(nom, valeur, affinages).values():
            for dork in dorks:
                assert termes_interdits(dork.query) == [], (nom, dork.query)
