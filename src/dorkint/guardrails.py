"""Garde-fous : aucun dork ne doit viser des credentials ou secrets de tiers (cf. PRODUCT.md)."""

import re

TERMES_INTERDITS: tuple[str, ...] = (
    "password",
    "passwd",
    "mot de passe",
    "mots de passe",
    "motdepasse",
    "credential",
    "credentials",
    "secret",
    "secrets",
    "api_key",
    "apikey",
    "token",
    "tokens",
    ".env",
    "id_rsa",
    "htpasswd",
    "private key",
    "wp-config",
    "dump",
    "combolist",
)

_MOTIF = re.compile(
    "|".join(rf"(?<![^\W_]){re.escape(t)}s?(?![^\W_])" for t in sorted(TERMES_INTERDITS, key=len, reverse=True)),
    re.IGNORECASE,
)


def termes_interdits(texte: str) -> list[str]:
    """Termes interdits présents dans `texte` (insensible à la casse), sans doublon."""
    return list(dict.fromkeys(m.group().lower() for m in _MOTIF.finditer(texte)))
