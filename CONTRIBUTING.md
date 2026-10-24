# CONTRIBUTING.md — dorkint

Pas de convention imposée (projet solo) : branches, commits et PR au choix,
message de commit clair suffit. Le suivi de tâches vit dans `crew/`.

## Règle de sécurité : pas de dorks credentials

Une contribution ne doit jamais ajouter de dork visant mots de passe, clés d'API,
tokens, fichiers de configuration sensibles ou bases de fuite. Le registre rejette
ces termes (`src/dorkint/guardrails.py`) et la CI échoue (`tests/test_guardrails.py`).

## Ajouter un mode

1. Écrire d'abord `tests/test_modes/test_<mode>.py` (mode enregistré, au moins un dork par catégorie, valeur entre guillemets, affinages croisés).
2. Créer `src/dorkint/modes/<mode>.py` avec un dict `CATEGORIES` (voir `AGENTS.md`, « Déclarer un mode »).
3. Ajouter le module à `MODES` dans `src/dorkint/modes/__init__.py`.
4. Sources France uniquement ; aucune catégorie credentials (`tests/test_guardrails.py` la refuse).
