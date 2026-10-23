# dorkint

Google dork generator for OSINT reconnaissance. You give it a value (name,
username, site, email...) and dorkint prints ready-to-open search links
(ctrl+click in the terminal), grouped by category.

dorkint **runs no search** and makes no network request: it only builds URLs.

## Responsible use

Reserved for targets you are authorized to examine (yourself, a consenting
person, a legitimate audit). No dork aimed at credentials, passwords or
sensitive configuration files is generated, and the registry rejects them.
Read [DISCLAIMER.md](DISCLAIMER.md) before use.

## Installation

Python 3.11 or later.

```bash
pip install .          # or: pipx install .
```

For development: `pip install -e .[dev]`.

## Usage

```bash
dorkint <mode> <value...> [--city CITY] [--company COMPANY] [--keyword WORD] [--out FILE] [--force]
```

| Mode | Primary value | Refinements |
|------|---------------|-------------|
| `fullname` | "John Smith" | `--city`, `--company` |
| `username` | username | `--city`, `--company` |
| `city` | city name | `--company` |
| `site` | domain (`example.fr`) | `--company` |
| `email` | email address | `--city`, `--company` |
| `phone` | French number | `--city`, `--company` |
| `company` | company name or SIREN | `--city` |

Examples (fictional values):

```bash
dorkint fullname John Smith --city Lyon      # quotes optional
dorkint site example.fr
dorkint company "Acme" --out links.txt
```

The output is a list of URLs, one per line, under `## Category` headers.
`--out` saves to a file and refuses to overwrite an existing file without
`--force`. Argument errors return exit code 2.

`dorkint --info` lists the dork patterns of each mode, by category, without
generating anything. A bracketed suffix shows what a pattern requires: a
refinement (`[--city]`) or a value derived from the primary value
(`[local, domain]`).

`--keyword` adds a quoted keyword to every dork to cross-reference
information (`dorkint username kalira --keyword minecraft`).

### Interactive version (menus)

`dorkint` alone (or `dorkint-tool`) opens numbered menus: pick the mode with
`1`, `2`, `3`..., enter the value, then the refinements and the keyword (ENTER
skips a field). `0` goes back; after the results you can save the links or run
another search in the same mode. Same engine as the flag-based CLI; it needs an
interactive terminal. Use `dorkint --help` for the help.

## Scope and limits

- France only for now (Infogreffe, societe.com, Pages Jaunes, data.gouv.fr,
  BODACC, Journal Officiel...). The dork patterns therefore contain French
  sites and French search words on purpose.
- The `phone` mode searches the 5 usual spellings of a French number; the
  `email` mode also searches the local part and the domain separately.
- Google results can be inaccurate or concern people with the same name.

## Adding a mode

A file `src/dorkint/modes/<mode>.py` calls `register(Mode(...))`: it is
discovered automatically, with no shared file to edit. Details and an example
in [AGENTS.md](AGENTS.md) ("Declaring a mode") and
[CONTRIBUTING.md](CONTRIBUTING.md).

## Development

```bash
python -m pytest -q     # tests
ruff check .            # lint
mypy src                # types
```

## License

[MIT](LICENSE).
