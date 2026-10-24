"""Mode `email`: public mentions of an email address (no leak database)."""

import re


def values(address):
    """`{local}`, `{domain}` and `{obfuscated}` (anti-spam spellings), only when the input is an address."""
    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[a-z]{2,}", address, re.IGNORECASE):
        return {}
    local, _, domain = address.partition("@")
    spelled = domain.replace(".", " dot ")
    forms = [f"{local} at {domain}", f"{local} [at] {domain}", f"{local} (at) {domain}", f"{local} at {spelled}"]
    return {
        "local": f'"{local}"',
        "domain": domain,
        "obfuscated": "(" + " OR ".join(f'"{f}"' for f in forms) + ")",
    }


CATEGORIES = {
    'Mentions web': [
        '{primary}',
        'intext:{primary}',
        '{primary} contact',
        '{primary} {city}',
        '{primary} {company}',
        '{primary} {company} {city}',
    ],
    'PDFs and documents': [
        'filetype:pdf {primary}',
        'filetype:doc OR filetype:docx {primary}',
        'filetype:xls OR filetype:xlsx OR filetype:ppt {primary}',
        'filetype:pdf {primary} {company}',
        'filetype:pdf {primary} {city}',
    ],
    'Social networks and profiles': [
        'site:linkedin.com {primary}',
        'site:facebook.com OR site:x.com OR site:instagram.com {primary}',
        'site:github.com OR site:gitlab.com {primary}',
        'site:linkedin.com {primary} {company}',
        'site:linkedin.com OR site:facebook.com {primary} {city}',
    ],
    'Git commits': [
        'site:github.com inurl:commit {primary}',
        'site:gitlab.com inurl:commit {primary}',
        'site:github.com inurl:commits {primary}',
        'site:bitbucket.org OR site:codeberg.org inurl:commit {primary}',
        'intext:"Author:" {primary} inurl:commit',
        'intext:"Signed-off-by:" {primary}',
        'intext:"Co-authored-by:" {primary}',
        'site:lore.kernel.org OR site:marc.info {primary}',
    ],
    'Forums and comments': [
        'inurl:forum {primary}',
        'site:reddit.com OR site:stackoverflow.com {primary}',
        'intext:{primary} inurl:comment',
        'inurl:forum {primary} {city}',
    ],
    'Directories and signatures': [
        'site:societe.com OR site:pagesjaunes.fr {primary}',
        'intitle:annuaire {primary}',
        '{primary} cordialement',
        '{primary} tél mobile signature',
        'site:pagesjaunes.fr {primary} {city}',
        'intitle:annuaire {primary} {company}',
    ],
    'Press and publications': [
        '{primary} communiqué de presse',
        '{primary} auteur publication',
        'site:hal.science OR site:researchgate.net {primary}',
        '{primary} communiqué {company}',
    ],
    'Local part and domain': [
        '{local} site:{domain}',
        '{local} -site:{domain}',
        'inurl:{primary}',
        'intitle:{primary}',
        '{primary} -site:linkedin.com -site:facebook.com',
        '{primary} -site:linkedin.com {company}',
    ],
    'Obfuscated forms': [
        '{obfuscated}',
        '{obfuscated} -site:{domain}',
        '{local} AROUND(5) {domain}',
        'intext:{local} site:{domain} (ext:pdf OR ext:docx)',
    ],
    'Operator crossings': [
        'allintext:{primary}',
        'allintitle:{primary}',
        'inanchor:{primary}',
        'intext:{primary} (ext:pdf OR ext:doc OR ext:docx OR ext:ppt OR ext:pptx OR ext:odt)',
        '{primary} (inurl:contact OR inurl:equipe OR inurl:team OR inurl:about)',
        '{primary} after:2023',
        '{primary} before:2015',
        'intext:{primary} {city} (ext:pdf OR ext:docx)',
        'allintext:{primary} {company}',
        '{primary} {company} (inurl:contact OR inurl:equipe OR inurl:team)',
    ],
}
