# Disclaimer and responsible use

## What dorkint does

dorkint is a search query generator. It runs no search, makes no network
request, and does not collect, store or transmit any data. It builds search
links that you open yourself in your browser.

## Authorized targets only

For use only on targets you are authorized to examine: yourself, a person who
has given consent, or an organization as part of a legitimate, documented audit
or engagement.

Using dorkint to harass, stalk, monitor, intimidate or impersonate a person, or
to publish their personal information (doxxing), is forbidden. See in
particular articles 226-1 et seq. and 222-33-2-2 et seq. of the French Penal
Code (to be checked on Légifrance).

## Personal data (GDPR)

Searching for information about an identifiable person is processing of
personal data within the meaning of the GDPR. As the user, you alone are
responsible for the lawfulness of that use (legal basis, purpose, minimization,
retention period, informing the people concerned) and for complying with
French and European law.

The file produced by `--out` contains the values you entered: it remains your
responsibility.

Data subjects can exercise their rights (objection, erasure, delisting) with
the source websites and the search engines, not with the author, who holds no
data.

## No credentials

dorkint deliberately generates no query aimed at credentials, passwords, keys
or sensitive configuration files across the web. A guardrail
(`src/dorkint/guardrails.py`) rejects these terms and a test fails if a mode
contains any.

The single exception: mode `site`, which audits one domain you are authorized
to examine, may expose a handful of templates that check for that domain's own
leaked secrets (`filetype:env`, `wp-config`, password-named log files...). Each
such template is explicitly opted in (`allow_credentials=True`) and is itself
anchored to `site:<domain>` — it can never run as a web-wide search. This is
surface self-audit of the authorized target, not third-party credential
hunting. Fraudulent access
to an automated data processing system is punished by articles 323-1 et seq. of
the French Penal Code.

## Scope

The scope is limited to France (French sources and platforms). No guarantee is
given for other jurisdictions.

## Reliability of results

Search engine results can be inaccurate, outdated or concern people with the
same name. Do not make any decision or take any action regarding a person on
this basis alone.

## Third-party search engines

Third-party search engines have their own terms of use, which you must comply
with. dorkint is not affiliated with any search engine. "Google" is a trademark
of Google LLC.

## Warranty

Software provided "as is", without warranty of any kind, express or implied,
including accuracy, completeness or fitness for a particular purpose. The
author cannot be held liable for damages resulting from its use, to the extent
permitted by law.

## Reporting

To report abuse, open an issue on the repository. Contributions aimed at
credentials or at targets outside the scope are rejected.
