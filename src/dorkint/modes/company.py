"""Mode `company`: company name or SIREN, French sources only."""

CATEGORIES = {
    'FR registers': [
        'site:infogreffe.fr {primary}',
        'site:societe.com {primary}',
        'site:pagesjaunes.fr {primary}',
        'site:pappers.fr {primary}',
        'site:annuaire-entreprises.data.gouv.fr {primary}',
        'site:societe.com {primary} {city}',
        'site:pagesjaunes.fr {primary} {city}',
    ],
    'data.gouv.fr and Journal Officiel / BODACC': [
        'site:data.gouv.fr {primary}',
        'site:bodacc.fr {primary}',
        'site:journal-officiel.gouv.fr {primary}',
        'site:bodacc.fr {primary} {city}',
    ],
    'Job offers': [
        'site:welcometothejungle.com {primary}',
        'site:indeed.fr {primary}',
        'site:linkedin.com/jobs {primary}',
        'site:apec.fr {primary}',
        'site:indeed.fr {primary} {city}',
    ],
    'Press and social networks': [
        'site:linkedin.com/company {primary}',
        'site:facebook.com {primary}',
        'site:x.com {primary}',
        '{primary} actualité presse',
        '{primary} {city} actualité presse',
    ],
    'Subdomains and exposed files': [
        '{primary} filetype:pdf',
        '{primary} filetype:xlsx OR filetype:docx',
        '{primary} inurl:intranet OR inurl:extranet',
        '{primary} {city} filetype:pdf',
    ],
    'Executives and officers': [
        '{primary} dirigeant OR président OR gérant',
        'site:pappers.fr {primary} dirigeants',
        'site:linkedin.com/in {primary} fondateur OR directeur',
        '{primary} {city} dirigeant',
    ],
}
