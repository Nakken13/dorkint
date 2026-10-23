# Avertissement et usage responsable

## Ce que fait dorkint

dorkint est un générateur de requêtes de recherche. Il n'exécute aucune
recherche, n'effectue aucune requête réseau, ne collecte, ne stocke ni ne
transmet aucune donnée. Il construit des liens de recherche que vous ouvrez
vous-même dans votre navigateur.

## Cibles autorisées uniquement

Usage réservé à des cibles que vous êtes autorisé à examiner : vous-même, une
personne ayant donné son consentement, ou une organisation dans le cadre d'un
audit ou d'une mission légitime et documentée.

Il est interdit d'utiliser dorkint pour harceler, traquer, surveiller,
intimider, usurper l'identité d'une personne, ou publier ses informations
personnelles (doxxing). Voir notamment les articles 226-1 et suivants et
222-33-2-2 et suivants du Code pénal (à vérifier sur Légifrance).

## Données personnelles (RGPD)

Rechercher des informations sur une personne identifiable constitue un
traitement de données à caractère personnel au sens du RGPD. En tant
qu'utilisateur, vous êtes seul responsable de la licéité de cet usage (base
légale, finalité, minimisation, durée de conservation, information des
personnes) et du respect de la loi française et européenne.

Le fichier produit par `--out` contient les valeurs que vous avez saisies : il
reste sous votre responsabilité.

Les personnes concernées peuvent exercer leurs droits (opposition, effacement,
déréférencement) auprès des sites sources et des moteurs de recherche, pas
auprès de l'auteur, qui ne détient aucune donnée.

## Pas de credentials

dorkint ne génère volontairement aucune requête visant des identifiants, mots
de passe, clés ou fichiers de configuration sensibles. Un garde-fou
(`src/dorkint/guardrails.py`) rejette ces termes et un test échoue si un mode en
contient. Les accès frauduleux à un système de traitement automatisé de données
sont réprimés par les articles 323-1 et suivants du Code pénal.

## Périmètre

Le périmètre est limité à la France (sources et plateformes françaises). Aucune
garantie n'est donnée pour d'autres juridictions.

## Fiabilité des résultats

Les résultats des moteurs de recherche peuvent être inexacts, obsolètes ou
concerner des homonymes. Ne prenez aucune décision ni action à l'égard d'une
personne sur cette seule base.

## Moteurs de recherche tiers

Les moteurs de recherche tiers ont leurs propres conditions d'utilisation, que
vous devez respecter. dorkint n'est affilié à aucun moteur de recherche.
« Google » est une marque de Google LLC.

## Garantie

Logiciel fourni « tel quel », sans garantie d'aucune sorte, expresse ou
implicite, notamment d'exactitude, d'exhaustivité ou d'adaptation à un usage
particulier. L'auteur ne saurait être tenu responsable des dommages résultant
de son utilisation, dans les limites permises par la loi.

## Signalement

Pour signaler un abus, ouvrez une issue sur le dépôt. Les contributions visant
des credentials ou des cibles hors périmètre sont refusées.
