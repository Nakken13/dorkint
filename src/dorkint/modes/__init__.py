"""One module per search mode: `CATEGORIES` (category -> query patterns) and optional `values(value)`."""

from dorkint.modes import city, company, email, fullname, phone, site, username

MODES = {
    "fullname": fullname,
    "username": username,
    "city": city,
    "site": site,
    "email": email,
    "phone": phone,
    "company": company,
}
