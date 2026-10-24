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
    'Operator crossings': [
        'site:{raw} (inurl:admin OR inurl:login OR inurl:signin OR inurl:dashboard OR inurl:portal)',
        'site:{raw} (inurl:test OR inurl:dev OR inurl:staging OR inurl:preprod OR inurl:beta)',
        'site:{raw} (ext:xml OR ext:json OR ext:yml OR ext:yaml)',
        'site:{raw} ext:php inurl:"?id="',
        'site:{raw} (inurl:upload OR inurl:uploads OR inurl:files) intitle:"index of"',
        'site:{raw} intitle:"index of" (ext:zip OR ext:tar OR ext:gz OR ext:7z)',
        'site:{raw} intitle:"index of" "last modified"',
        'site:{raw} ("powered by WordPress" OR "powered by Joomla" OR "powered by Drupal")',
        'site:{raw} inurl:wp-content ext:pdf',
        'site:{raw} (inurl:swagger OR inurl:api-docs OR intitle:"swagger")',
        'site:{raw} intitle:"phpinfo()"',
        'site:{raw} after:2024',
        'site:{raw} before:2018 ext:pdf',
    ],
    'Wildcard subdomains': [
        'site:*.{raw} -site:www.{raw}',
        'site:*.{raw} (inurl:dev OR inurl:staging OR inurl:test OR inurl:preprod OR inurl:beta)',
        'site:*.{raw} (intitle:login OR intitle:admin OR intitle:portal)',
        'site:*.{raw} (inurl:vpn OR inurl:mail OR inurl:webmail OR inurl:remote)',
    ],
    'Emails and contacts': [
        'site:{raw} intext:"@{raw}"',
        'site:{raw} ext:pdf intext:"@{raw}"',
        'site:{raw} (inurl:contact OR inurl:equipe OR inurl:team OR inurl:about) intext:"@"',
        '-site:{raw} intext:"@{raw}"',
    ],
    'Cloud storage mentions': [
        'site:s3.amazonaws.com "{raw}"',
        'site:blob.core.windows.net "{raw}"',
        'site:storage.googleapis.com "{raw}"',
        'site:drive.google.com "{raw}"',
        'site:docs.google.com "{raw}"',
        'site:trello.com "{raw}"',
        'site:pastebin.com "{raw}"',
    ],
}
