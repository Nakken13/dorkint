"""One module per search mode: `CATEGORIES` (category -> query patterns) and optional `values(value)`."""

from dorkint.modes import company, email, fullname, phone, site, username

MODES = {
    "fullname": fullname,
    "username": username,
    "site": site,
    "email": email,
    "phone": phone,
    "company": company,
}


def dork_counts() -> dict[str, int]:
    """Number of dork patterns per mode, computed from the mode modules (never hard-coded)."""
    return {name: sum(len(patterns) for patterns in mode.CATEGORIES.values()) for name, mode in MODES.items()}
