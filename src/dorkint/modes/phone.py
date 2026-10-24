"""Mode `phone`: French phone number."""

import re

_FR = re.compile(r"^(?:0|\+?33|0033)(\d{9})$")


def values(number):
    """`{primary}` becomes `("a" OR "b" ...)` over the equivalent formats of a FR number."""
    raw = re.sub(r"[\s.\-()]", "", number.replace("(0)", ""))
    match = _FR.match(raw)
    if not match:
        return {}
    n = match.group(1)  # 9 digits without the leading 0
    pairs = [n[i:i + 2] for i in range(1, 9, 2)]
    formats = [
        f"0{n[0]} {' '.join(pairs)}",
        f"0{n[0]}.{'.'.join(pairs)}",
        f"0{n}",
        f"+33 {n[0]} {' '.join(pairs)}",
        f"+33{n}",
    ]
    return {"primary": "(" + " OR ".join(f'"{f}"' for f in formats) + ")"}


CATEGORIES = {
    'Reverse directories': [
        'site:pagesjaunes.fr {primary}',
        'site:118712.fr {primary}',
        'site:pagesjaunes.fr {primary} {city}',
        'site:118712.fr {primary} {city}',
    ],
    'Mentions web': [
        '{primary}',
        '{primary} {city}',
        '{primary} {company}',
        '{primary} {city} {company}',
    ],
    'Social networks': [
        'site:facebook.com {primary}',
        'site:linkedin.com {primary}',
        'site:twitter.com OR site:instagram.com {primary}',
        'site:linkedin.com {primary} {company}',
    ],
    'Classifieds': [
        'site:leboncoin.fr {primary}',
        'site:vinted.fr {primary}',
        'site:leboncoin.fr {primary} {city}',
    ],
    'Documents': [
        'filetype:pdf {primary}',
        'filetype:doc OR filetype:docx {primary}',
        'filetype:pdf {primary} {city}',
        'filetype:pdf {primary} {company}',
    ],
    'Company sites': [
        'intext:contact {primary}',
        'inurl:contact {primary}',
        'intext:contact {primary} {company}',
        'inurl:contact {primary} {city}',
    ],
    'Operator crossings': [
        '{primary} (ext:pdf OR ext:docx OR ext:xlsx OR ext:pptx)',
        '{primary} (inurl:contact OR inurl:mentions-legales OR inurl:cgv OR inurl:a-propos)',
        '{primary} (intitle:contact OR intitle:"mentions légales")',
        '{primary} (intext:fax OR intext:mobile OR intext:tél)',
        '{primary} -site:pagesjaunes.fr -site:118712.fr -site:facebook.com -site:linkedin.com',
        '{primary} after:2023',
        '{primary} before:2015',
        '{primary} {city} (ext:pdf OR ext:docx)',
        '{primary} {company} (inurl:contact OR inurl:equipe)',
    ],
    'Caller reports': [
        'site:tellows.fr {primary}',
        '{primary} (avis OR arnaque OR démarchage OR appel)',
        '{primary} (avis OR arnaque OR démarchage) -site:tellows.fr',
    ],
}
