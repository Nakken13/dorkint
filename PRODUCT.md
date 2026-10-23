# PRODUCT.md — dorkint

## Vision

Dorkint est un outil CLI qui **génère** des requêtes Google dorks légitimes
(reconnaissance OSINT) selon le type de cible recherchée, pour éviter de les
écrire à la main. Il ne scrape rien et n'exécute aucune recherche lui-même :
il construit des requêtes, l'utilisateur les ouvre lui-même dans son
navigateur. Projet solo, destiné à être publié en open source comme pièce de
portfolio pour une candidature en école d'ingénieur cyber.

## Utilisateur cible

L'auteur lui-même, pour de la reconnaissance OSINT sur des cibles qu'il est
autorisé à regarder (lui-même, des cibles consentantes, des audits dans un
cadre légitime). Une fois open source, tout utilisateur du CLI reste
responsable de l'usage qu'il en fait — dorkint ne génère que des requêtes de
recherche publique, jamais de requêtes orientées extraction d'identifiants/
credentials.

## Scope actuel

Rien de livré : projet à l'état de scaffold, langage non encore choisi (C++,
Python ou Java envisagés).

Périmètre fonctionnel déjà défini par brainstorming :

- 7 modes de recherche au lancement : `nom prénom`, `username`, `ville`,
  `site`, `mail`, `tel`, `entreprise`.
- Pour chaque mode, un champ principal obligatoire + champs d'affinage
  optionnels (ex. `nom prénom` + `ville`/`entreprise` connues) qui enrichissent
  les dorks générés par des variantes croisées.
- Chaque mode a un set de catégories de dorks dédié (réseaux sociaux, CV/PDF
  nominatifs, travaux académiques, interventions publiques, actes publics,
  portfolios, presse, sous-domaines, fichiers exposés par erreur, offres
  d'emploi, etc. — détail par mode à affiner à l'implémentation).
- Scope géographique : **France uniquement** pour le moment (plateformes/
  sources FR : Infogreffe, societe.com, Pages Jaunes, data.gouv.fr, Journal
  Officiel... — pas d'équivalents internationaux pour l'instant).
- Sortie : liste de liens Google cliquables affichée dans le terminal
  (ctrl+clic pour ouvrir), avec option de sauvegarde dans un fichier.
- Pas d'exécution de recherche ni d'appel à une API de search (Google Custom
  Search, Bing, Brave, SerpApi...) — décision prise après comparatif : toutes
  ces API sont soit fermées aux nouveaux comptes/retirées, soit payantes, et
  sortent du scope "générateur de dorks".

## Hors scope (explicitement)

- **Pas d'exécution de recherche automatisée** (ni scraping direct de Google,
  ni API de search tierce) — dorkint reste un générateur de requêtes, jamais
  un moteur d'exécution.
- **Pas de dorks orientés extraction de credentials/mots de passe/fichiers de
  config sensibles de tiers non consentants** — seules des catégories de
  reconnaissance de surface légitime (exposition publique, fuite accidentelle
  signalée de façon générique) sont couvertes. Exception unique, scopée : le
  mode `site` (audit d'un domaine autorisé) peut inclure quelques templates
  de fuite de secrets *du site audité lui-même*, toujours ancrés
  `site:{primary:raw}` et marqués explicitement `allow_credentials=True`
  (`src/dorkint/guardrails.py`) — jamais une recherche web-wide.
- **Pas de plateformes/sources hors France** pour l'instant (à revisiter plus
  tard si besoin).
