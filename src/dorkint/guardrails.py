"""Guardrails: no dork may target third-party credentials or secrets (see PRODUCT.md)."""

import re

FORBIDDEN_TERMS: tuple[str, ...] = (
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

_PATTERN = re.compile(
    "|".join(rf"(?<![^\W_]){re.escape(t)}s?(?![^\W_])" for t in sorted(FORBIDDEN_TERMS, key=len, reverse=True)),
    re.IGNORECASE,
)


def forbidden_terms(text: str) -> list[str]:
    """Forbidden terms present in `text` (case-insensitive), without duplicates."""
    return list(dict.fromkeys(m.group().lower() for m in _PATTERN.finditer(text)))
