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
dorkint <mode> <value...> [--city CITY] [--company COMPANY] [--out FICHIER] [--force]
```

| Mode | Valeur principale | Affinages |
|------|-------------------|-----------|
| `fullname` | « Jean Dupont » | `--city`, `--company` |
| `username` | pseudo | `--city`, `--company` |
| `city` | nom de ville | `--company` |
| `site` | domaine (`exemple.fr`) | `--company` |
| `email` | adresse mail | `--city`, `--company` |
| `phone` | numéro français | `--city`, `--company` |
| `company` | raison sociale ou SIREN | `--city` |

Exemples (valeurs fictives) :

```bash
dorkint fullname Jean Dupont --city Lyon     # guillemets facultatifs
dorkint site exemple.fr
dorkint company "Acme" --out liens.txt
```

La sortie est une liste d'URL, une par ligne, sous des en-têtes `## Catégorie`.
`--out` sauvegarde dans un fichier et refuse d'écraser un fichier existant sans
`--force`. Les erreurs d'arguments retournent le code 2.

`dorkint --info` liste les patrons de dorks de chaque mode, par catégorie, sans rien
générer. Un suffixe entre crochets indique ce qu'un patron exige : un affinage
(`[--city]`) ou une valeur dérivée de la valeur principale (`[local, domaine]`).

## Périmètre et limites

- France uniquement pour l'instant (Infogreffe, societe.com, Pages Jaunes,
  data.gouv.fr, BODACC, Journal Officiel...).
- Le mode `phone` cherche les 5 écritures usuelles d'un numéro français ; le mode `email` cherche aussi la partie locale et le domaine séparément.
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
