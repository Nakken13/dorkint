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

Un fichier `src/dorkint/modes/<mode>.py` + une ligne dans `MODES` (`modes/__init__.py`,
qui sert aussi de liste des sous-commandes CLI). Pas de classe : un dict de patrons.

```python
CATEGORIES = {
    "Réseaux sociaux": [
        "site:linkedin.com/in {primary}",
        "site:linkedin.com/in {primary} {city}",
    ],
}
```

- `{primary}`, `{city}`, `{company}` sont insérés entre guillemets ; `{raw}` = la valeur telle quelle.
- Un patron n'est généré que si tous ses placeholders ont une valeur ; les affinages d'un mode sont déduits de ses patrons.
- `values(value)` (optionnel) : renvoie des placeholders en plus ou en remplacement (`modes/phone.py` : `{primary}` devient `("a" OR "b")`, limite Google ~32 mots ; `modes/email.py` : `{local}` / `{domain}`).
- Tests du mode : `tests/test_modes/test_<mode>.py` ; jamais de catégorie credentials.

## Garde-fou credentials

`tests/test_guardrails.py` échoue si une catégorie ou un patron d'un mode contient un
terme de `dorkint.guardrails.FORBIDDEN_TERMS` (password, secret, token, .env,
id_rsa, dump...). Dorkint ne cible jamais credentials ni secrets de tiers
(`PRODUCT.md`, hors scope). Pour ajouter un terme : l'ajouter à la liste ; ce test
global vérifie tous les modes (seule exception : patrons `site:{raw} ...` du mode `site`).
