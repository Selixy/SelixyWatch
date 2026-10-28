# partage

Invitations par lien et partages d'un nœud (dossier ou playlist) avec d'autres comptes. Routes dans `routes.py` (`ROUTES_GET`, `ROUTES_POST`).

## Décisions

- Le jeton (`secrets.token_urlsafe(24)`) n'est jamais stocké : seul son sha256 l'est (`jeton_hash`). Il voyage dans le fragment `#` du lien
  pour ne pas apparaître dans les journaux nginx. L'`id` d'invitation (`token_hex(6)`) sert à la révocation et à l'affichage.
- Un lien couvre 1 à 50 nœuds (table `invitation_noeuds`), tous dont le créateur est propriétaire (sinon rien n'est créé). Rôle unique :
  `editeur` (la colonne `invitations.role` est conservée mais toujours `editeur` ; `invitations.noeud_id` a été supprimée par la migration 005,
  qui a repris les anciennes invitations dans `invitation_noeuds`). Plus de route `inviter` par nœud ni de changement de rôle.
- Acceptation (`acceptation.py`) : pour chaque nœud du lien (les nœuds supprimés disparaissent par cascade), on regarde si le compte est déjà
  éditeur ou propriétaire (accès hérité compris). Si aucun nœud n'est à créer : `deja: true`, aucun usage consommé, même lien expiré ou épuisé.
  Sinon 410 si expiré/épuisé, sinon un usage consommé puis un partage éditeur créé (ou relevé de lecteur) pour chaque nœud manquant, dans une
  seule transaction. Un lien sans aucun nœud restant donne 404 (voir comme accepter).
- La consommation est un `UPDATE ... WHERE usages < usages_max AND expire_le > now() RETURNING` : sur le dernier usage, la seconde transaction
  attend le verrou de ligne, relit la ligne validée et ne trouve plus rien (410). Un seul gagnant.
- Acceptation : `copie.py` copie dans `rangements` l'arborescence de chaque nœud nouvellement accordé (noms et structure du moment), la racine
  posée à la racine du compte à la suite de ses racines ; ensuite chacun range et nomme à sa guise. Retirer/quitter supprime ces lignes.
- Le partage ne fait que monter : lecteur vers éditeur, jamais l'inverse (`ON CONFLICT ... WHERE EXCLUDED.role = 'editeur'`).
- Limite connue : deux acceptations simultanées du même compte pour le même jeton peuvent consommer deux usages (rare, sans conséquence
  sur les droits).
- Les droits viennent de `acces.droits` : gérer = `proprietaire`. Un éditeur invité ne peut donc pas inviter.
- `quitter` n'est permis qu'à la racine d'un partage reçu, c'est-à-dire là où existe la ligne de `partages` ; ailleurs 400.
- Avant tout retrait d'accès, les comptes concernés sont calculés (`concernes`) puis signalés après la validation de la transaction.

## Pièges

- `GET /api/partage?noeud=<id>` et non `/api/partage/<id>` : le routeur GET fait une correspondance exacte du chemin et ne gère pas `Refus` ;
  `lire` attrape donc `Refus` elle-même.
- `comptes.profils.publics` et `diffusion.bibliotheque.signaler` sont fournis par d'autres domaines ; les tests les simulent.

## Lien qui offre le statut Pro

`POST /api/invitations` accepte `pro: true`, réservé aux administrateurs (403 sinon) ; colonne `invitations.donne_pro` (migration 006).
À l'acceptation, un compte non éphémère et pas encore Pro passe Pro (quota porté à 20 Go au moins, `offre_pro.py`), même s'il avait
déjà accès aux éléments (un usage est alors consommé). Un compte éphémère ne devient jamais Pro. L'envoi de fichiers reste soumis à
l'e-mail validé, comme pour tout Pro. `voir` renvoie `pro` pour que la page d'invitation l'annonce.
