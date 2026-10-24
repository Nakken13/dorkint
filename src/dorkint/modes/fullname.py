"""Mode `fullname`: public information about a person (FR sources)."""

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
}
