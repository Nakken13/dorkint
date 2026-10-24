"""Mode `fullname`: public information about a person (FR sources)."""

import unicodedata


def _ascii(word):
    return unicodedata.normalize("NFKD", word).encode("ascii", "ignore").decode().lower()


def values(name):
    """`{first}`, `{last}` and their URL forms `{slug}` / `{dotted}`, when the name has 2+ words.

    For exactly two words `{primary}` becomes two separate quoted terms (`"john" "doe"`): the names
    match in any order and with words in between. Google ignores case, so no case variants.
    """
    words = name.split()
    if len(words) < 2:
        return {}
    first, last = words[0], words[-1]
    result = {"first": first, "last": last}
    if len(words) == 2:
        result["primary"] = f'"{first}" "{last}"'
    if (a := _ascii(first)) and (b := _ascii(last)):
        result |= {"slug": f"{a}-{b}", "dotted": f"{a}.{b}"}
    return result


CATEGORIES = {
    'Social networks': [
        'site:linkedin.com/in {primary}',
        'site:linkedin.com/in {primary} {city}',
        'site:linkedin.com/in {primary} {company}',
        'site:facebook.com {primary}',
        'site:facebook.com {primary} {city}',
        'site:instagram.com {primary}',
        '(site:x.com OR site:twitter.com) {primary}',
        '(site:x.com OR site:twitter.com) {primary} {city}',
        'site:github.com {primary}',
        'site:github.com {primary} {company}',
    ],
    'Named CVs and PDFs': [
        'filetype:pdf {primary} cv',
        'filetype:pdf {primary} curriculum vitae',
        'filetype:pdf {primary} cv {city}',
        'filetype:pdf {primary} cv {company}',
        'filetype:pdf {primary} {city} {company}',
    ],
    'Academic work': [
        'site:theses.fr {primary}',
        'site:hal.science {primary}',
        'filetype:pdf {primary} mémoire',
        'site:hal.science {primary} {company}',
        'filetype:pdf {primary} mémoire {city}',
    ],
    'Public appearances': [
        '{primary} conférence intervenant',
        'site:meetup.com {primary}',
        'site:youtube.com {primary}',
        '{primary} conférence {city}',
        'site:youtube.com {primary} {company}',
    ],
    'Public records': [
        'site:journal-officiel.gouv.fr {primary}',
        'site:bodacc.fr {primary}',
        'site:data.gouv.fr {primary}',
        'site:bodacc.fr {primary} {city}',
        'site:bodacc.fr {primary} {company}',
    ],
    'Portfolios': [
        '(site:behance.net OR site:dribbble.com) {primary}',
        '{primary} portfolio',
        '{primary} portfolio {city}',
        '{primary} portfolio {company}',
    ],
    'Press': [
        '{primary} interview OR article',
        'site:lemonde.fr OR site:lefigaro.fr OR site:liberation.fr {primary}',
        '{primary} {city} article',
        '{primary} {company} interview',
        '{primary} {city} {company}',
    ],
    'Name variants': [
        '"{first} * {last}"',
        '"{last} {first}"',
        '"{last}, {first}"',
        '"{first}" AROUND(3) "{last}"',
        'inurl:{slug}',
        'inurl:{dotted}',
        'site:linkedin.com/in inurl:{slug} -inurl:dir',
    ],
    'Operator crossings': [
        'allintext:{phrase} email contact',
        'allintitle:{phrase}',
        'intitle:{phrase} (ext:pdf OR ext:doc OR ext:docx OR ext:odt)',
        'intext:{phrase} (inurl:cv OR inurl:resume OR inurl:curriculum)',
        'inanchor:{phrase}',
        '{primary} after:2023',
        '{primary} before:2015',
        '{primary} -site:linkedin.com -site:facebook.com -site:instagram.com -site:x.com',
        '{primary} (intext:@gmail.com OR intext:@outlook.fr OR intext:@yahoo.fr OR intext:@hotmail.fr)',
        'site:linkedin.com/in -inurl:dir {primary} (Current OR Actuel OR Previous OR Précédent)',
        'ext:pdf {primary} {city}',
        'allintext:{phrase} {city}',
        '{primary} {company} (ext:pdf OR ext:pptx)',
        'intitle:{phrase} {company}',
        'inanchor:{phrase} {company}',
        'site:linkedin.com/in -inurl:dir {primary} {company} (Current OR Actuel OR Previous OR Précédent)',
    ],
}
