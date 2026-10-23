# dorkint

Générateur de Google dorks pour la reconnaissance OSINT. Vous donnez une
valeur (nom, pseudo, site, mail...), dorkint affiche des liens de recherche
prêts à ouvrir (ctrl+clic dans le terminal), classés par catégorie.

dorkint **n'exécute aucune recherche** et ne fait aucune requête réseau : il
construit seulement des URL.

## Usage responsable

Réservé à des cibles que vous êtes autorisé à examiner (vous-même, une personne
consentante, un audit légitime). Aucun dork visant des identifiants, mots de
passe ou fichiers de configuration sensibles n'est généré, et le registre les
refuse. Lisez [DISCLAIMER.md](DISCLAIMER.md) avant utilisation.

## Installation

Python 3.11 ou plus.

```bash
pip install .          # ou : pipx install .
```

Pour développer : `pip install -e .[dev]`.

## Utilisation

```bash
dorkint <mode> <valeur> [--ville VILLE] [--entreprise ENTREPRISE] [--out FICHIER] [--force]
```

| Mode | Valeur principale | Affinages |
|------|-------------------|-----------|
| `nom-prenom` | « Jean Dupont » | `--ville`, `--entreprise` |
| `username` | pseudo | `--ville`, `--entreprise` |
| `ville` | nom de ville | `--entreprise` |
| `site` | domaine (`exemple.fr`) | `--entreprise` |
| `mail` | adresse mail | `--ville`, `--entreprise` |
| `tel` | numéro français | `--ville`, `--entreprise` |
| `entreprise` | raison sociale ou SIREN | `--ville` |

Exemples (valeurs fictives) :

```bash
dorkint nom-prenom "Jean Dupont" --ville Lyon
dorkint site exemple.fr
dorkint entreprise "Acme" --out liens.txt
```

La sortie est une liste d'URL, une par ligne, sous des en-têtes `## Catégorie`.
`--out` sauvegarde dans un fichier et refuse d'écraser un fichier existant sans
`--force`. Les erreurs d'arguments retournent le code 2.

## Périmètre et limites

- France uniquement pour l'instant (Infogreffe, societe.com, Pages Jaunes,
  data.gouv.fr, BODACC, Journal Officiel...).
- Le mode `tel` ne cible que le format saisi, pas les autres écritures du numéro.
- Le mode `mail` ne cherche pas séparément le nom d'utilisateur et le domaine.
- Les résultats de Google peuvent être inexacts ou concerner des homonymes.

## Ajouter un mode

Un fichier `src/dorkint/modes/<mode>.py` appelle `register(Mode(...))` : il est
découvert automatiquement, sans éditer de fichier partagé. Détails et exemple
dans [AGENTS.md](AGENTS.md) (« Déclarer un mode ») et
[CONTRIBUTING.md](CONTRIBUTING.md).

## Développement

```bash
python -m pytest -q     # tests
ruff check .            # lint
mypy src                # types
```

## Licence

[MIT](LICENSE).
