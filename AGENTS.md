# AGENTS.md — dorkint

Guide invariants + repo map pour tout agent (Claude Code ou autre) travaillant
sur ce projet.

## Stack

Outil CLI. Langage **non encore choisi** (C++, Python ou Java envisagés). Aucun
manifeste présent ; mettre à jour cette section dès le choix fait.

## Repository map

```text
crew/   suivi de tâches (scaffold claude-crew)
```

Aucun code source pour l'instant.

## Commandes vérifiées

Aucune : pas de code ni de manifeste. À renseigner (install, run, tests, build)
une fois la stack choisie et les commandes exécutées avec succès.

## Règles de code

Pas de conventions spécifiques tant que la stack n'est pas choisie.

## Secrets and boundaries

Pas d'authentification ni de donnée sensible prévues. Ne jamais committer de
fichier `.env` ni de clé d'API si une est ajoutée plus tard.

## Documentation routing

- Vision produit / scope : `PRODUCT.md`.
- Conventions de contribution : `CONTRIBUTING.md`.
- Guide global de contexte : `crew/CLAUDE_CONTEXT/AGENTS.md`.

## Déclarer un mode

Un fichier `src/dorkint/modes/<mode>.py` (tirets du nom CLI → underscores),
découvert automatiquement par `builder.load_modes()` : aucun fichier partagé à
éditer.

```python
from dorkint.builder import Category, Mode, Template, register

register(Mode(
    name="fullname",                 # nom de la sous-commande CLI
    refinements=("city", "company"),
    categories=(
        Category("Réseaux sociaux", (
            Template("site:linkedin.com/in {principal}"),
            Template("site:linkedin.com/in {principal} {city}", requires=("city",)),
        )),
    ),
))
```

- `{principal}`, `{city}`... sont insérés entre guillemets ; `{x:raw}` sans guillemets.
- `requires` : le patron n'est généré que si tous ces affinages sont fournis.
- `Mode(variantes=fn)` : `{principal}` devient `("a" OR "b")` (ex. écritures d'un numéro, `modes/tel.py`) ; `{principal:raw}` ignore les variantes ; limite Google ~32 mots par requête.
- `Mode(derive=fn, derived=("local",...))` : valeurs calculées utilisables comme `{local}` / `requires` (ex. `modes/mail.py`).
- Tests du mode : `tests/test_modes/test_<mode>.py` ; jamais de catégorie credentials.

## Garde-fou credentials

`builder.register` refuse tout mode dont une catégorie ou un template contient un
terme de `dorkint.guardrails.TERMES_INTERDITS` (password, secret, token, .env,
id_rsa, dump...). Dorkint ne cible jamais credentials ni secrets de tiers
(`PRODUCT.md`, hors scope). Pour ajouter un terme : l'ajouter à la liste ; un test
global (`tests/test_guardrails.py`) vérifie tous les modes chargés.
