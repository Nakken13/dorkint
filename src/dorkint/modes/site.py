"""Mode `site`: surface reconnaissance of a domain you are authorized to audit."""

CATEGORIES = {
    'Subdomains': [
        'site:*.{raw} -www',
        'site:*.*.{raw} -www',
    ],
    'Visible login and admin pages': [
        'site:{raw} inurl:login',
        'site:{raw} inurl:admin',
        'site:{raw} intitle:"espace client" OR intitle:"espace membre"',
    ],
    'Exposed documents': [
        'site:{raw} filetype:pdf',
        'site:{raw} filetype:doc OR filetype:docx',
        'site:{raw} filetype:xls OR filetype:xlsx',
        'site:{raw} filetype:ppt OR filetype:pptx',
        'site:{raw} filetype:pdf "confidentiel"',
        'site:{raw} filetype:pdf "usage interne"',
    ],
    'Directory listings': [
        'site:{raw} intitle:"index of"',
        'site:{raw} intitle:"index of" "parent directory"',
    ],
    'Sensitive files exposed on the site': [
        'site:{raw} intitle:"index of" (filetype:sql OR filetype:log OR filetype:bak)',
        'site:{raw} (ext:git OR ext:svn) intitle:"index of"',
        'site:{raw} filetype:env "DB_PASSWORD"',  # allow_credentials
        'site:{raw} inurl:"wp-config" (filetype:txt OR filetype:bak)',  # allow_credentials
        'site:{raw} filetype:log inurl:"password"',  # allow_credentials
    ],
    'Error pages and technologies': [
        'site:{raw} "page not found" OR "page introuvable"',
        'site:{raw} "powered by"',
        'site:{raw} intitle:"error" OR intitle:"error"',
    ],
    'Mentions elsewhere': [
        '-site:{raw} "{raw}"',
        '-site:{raw} "{raw}" avis OR critiques',
        '-site:{raw} {primary} {company}',
    ],
    'Job offers': [
        'site:{raw} inurl:careers OR inurl:carrieres OR inurl:recrutement',
        'site:{raw} "offre d\'emploi" OR "nous recrutons"',
        'site:linkedin.com/jobs OR site:indeed.fr {company}',
    ],
    'Press': [
        '-site:{raw} "{raw}" presse OR communiqué',
        '"{raw}" intitle:interview OR intitle:article',
        '{company} "{raw}" actualités',
    ],
}
