import pytest

from dorkint import builder
from dorkint.builder import Category, Dork, DorkintError, Mode, Template, generer


@pytest.fixture
def fake_mode(monkeypatch: pytest.MonkeyPatch) -> Mode:
    mode = Mode(
        name="fake",
        refinements=("ville", "entreprise"),
        categories=(
            Category("Base", (Template('site:exemple.fr {principal}'),)),
            Category(
                "Croisé",
                (
                    Template("{principal} {ville}", requires=("ville",)),
                    Template("{principal} {ville} {entreprise}", requires=("ville", "entreprise")),
                ),
            ),
            Category("Brut", (Template("site:{principal:raw}"),)),
        ),
    )
    monkeypatch.setitem(builder._REGISTRY, "fake", mode)
    return mode


def test_placeholder_is_quoted(fake_mode: Mode) -> None:
    result = generer("fake", "Jean Dupont", {})
    assert result["Base"] == [Dork("Base", 'site:exemple.fr "Jean Dupont"')]


def test_raw_placeholder_is_not_quoted(fake_mode: Mode) -> None:
    assert generer("fake", "exemple.fr", {})["Brut"][0].query == "site:exemple.fr"


def test_quotes_in_value_are_removed(fake_mode: Mode) -> None:
    assert generer("fake", 'Jean "le" Dupont', {})["Base"][0].query == 'site:exemple.fr "Jean le Dupont"'


def test_absent_refinement_gives_only_base_dorks(fake_mode: Mode) -> None:
    assert "Croisé" not in generer("fake", "Jean", {})
    assert "Croisé" not in generer("fake", "Jean", {"ville": None, "entreprise": ""})


def test_present_refinement_adds_cross_variants(fake_mode: Mode) -> None:
    queries = [d.query for d in generer("fake", "Jean", {"ville": "Lyon"})["Croisé"]]
    assert queries == ['"Jean" "Lyon"']
    both = [d.query for d in generer("fake", "Jean", {"ville": "Lyon", "entreprise": "Acme"})["Croisé"]]
    assert both == ['"Jean" "Lyon"', '"Jean" "Lyon" "Acme"']


def test_empty_principal_rejected(fake_mode: Mode) -> None:
    with pytest.raises(DorkintError, match="vide"):
        generer("fake", "   ", {})


def test_unknown_mode_rejected() -> None:
    with pytest.raises(DorkintError, match="inconnu"):
        generer("nexistepas", "x", {})


def test_unsupported_refinement_rejected(fake_mode: Mode) -> None:
    with pytest.raises(DorkintError, match="affinage"):
        generer("fake", "x", {"telephone": "1"})


def test_template_with_undeclared_placeholder_rejected() -> None:
    with pytest.raises(DorkintError, match="ville"):
        Template("{principal} {ville}")


def test_mode_without_categories_rejected() -> None:
    with pytest.raises(DorkintError, match="catégorie"):
        Mode("vide", (), ())


def test_duplicate_queries_are_dropped(monkeypatch: pytest.MonkeyPatch) -> None:
    mode = Mode("dup", (), (Category("A", (Template("{principal}"), Template("{principal}"))),))
    monkeypatch.setitem(builder._REGISTRY, "dup", mode)
    assert len(generer("dup", "x", {})["A"]) == 1


def test_register_rejects_duplicate_name(fake_mode: Mode) -> None:
    with pytest.raises(DorkintError, match="déjà"):
        builder.register(fake_mode)


def test_modes_discovered_from_package(tmp_path: object) -> None:
    # le chargement automatique ne doit pas échouer sur le package modes (même vide)
    builder.load_modes()
