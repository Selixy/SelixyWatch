# css

Feuilles du socle. Celles de la room sont décrites plus bas ; `playlists.css` charge avec sa page. Ordre de chargement : `tokens.css`,
`base.css`, `surfaces.css`, `header.css`, puis la feuille de la page.

- `base.css` : remise à zéro, mise en page, boutons, avatars ; couleurs uniquement via `tokens.css`. `overscroll-behavior: none` évite
  le rebond de page et l'actualisation par glissé ; `touch-action: manipulation` évite le zoom par double-toucher. Le fond du `body`
  est transparent : il est peint sur la racine par `surfaces.css`.
- `surfaces.css` : jetons « verre » (`--verre*`, `--flou`, `--halo*`, `--degrade*`), chargés après `tokens.css`. Tout ce qui est
  translucide passe par eux ; le repli opaque (`@supports not`) est en fin de fichier : jamais de texte sur un fond qui transparaît.
  Le fond (lueurs douces fixes, que le verre floute) est peint sur la racine jusqu'au bas du grand viewport (`100lvh`) : sur
  téléphone il passe sous l'encoche et sous la barre de Safari sans coupure (`background-attachment: fixed` est ignoré par iOS).
  Dans la coque, les cadres sont transparents (`:root.cadre`) : on voit le fond de la coque. Le texte blanc sur `--degrade` a un
  contraste d'au moins 6:1 ; en sombre le dégradé est clair et le texte sombre.
- `header.css` : barre de verre flottante, onglets centrés, pastille « segmentée » pour la page courante ; le rond coupe ou rétablit le son. Positionnée en `fixed` au-dessus des vues pour que le contenu remonte dessous avec flou d'arrière-plan au défilement. Sur
  téléphone, même barre sans le nom (pas la place).
- `jauge.css` : la jauge du volume général dans l'en-tête, qui remplace le mot de la marque au survol.
- `preparation.css` : le voile de préparation sur l'image du lecteur (voir `js/lecteur/preparation.js`). Le fond de l'état « vide » (`#0a0910`, dans `ecran.css`) est la couleur opaque du voile (`preparation.css`) : à garder identique, sinon la teinte saute quand le voile arrive. Le voile est opaque pour cacher ce que le lecteur affiche dessous pendant qu'il se prépare.
- `coque.css` : l'en-tête flotte au-dessus, la coque et ses cadres occupent tout l'écran (`position: absolute; inset: 0`). Les vues défilent sous l'en-tête sans coupure nette. Une vue masquée reste chargée et visible pour le navigateur (`visibility`, pas
  `display`) : son lecteur continue de jouer. Le contenu reste dans les zones sûres et suit le clavier (`--hauteur`, `--decalage`
  viennent de `coque.js`). Le décalage de `body` n'est appliqué que quand iOS fait glisser la page (classe `decale`). La molette sur l'en-tête est retransmise au cadre actif.
- `login.css` : profil, une grande carte de verre arborant le logotype de la marque, avatar entouré d'un anneau dégradé.
- `compte.css` : modes connexion/inscription, quota, appareils connectés, zone de suppression du profil. `invitation.css` : page d'invitation, aussi pages de confirmation et de récupération. `compte.css` porte aussi le lien discret « Mot de passe oublié ? » et la mention d'envoi réservé.

## Feuilles de la room

La page `room/index.html` charge, dans cet ordre, les feuilles du lecteur, qui remplacent l'ancien `lecteur.css` :
`salle`, `ecran`, `commandes`, `reactions`, `presence-base`, `presence-video`, `presence-menu`, `presence-animations`,
`presence-disposition`, `file`, `chat`, `notifications`, `telephone`, `plein`.

**L'ordre compte.** Les règles de même spécificité se départagent à l'ordre de chargement, comme dans l'ancien fichier unique :

- `salle.css` vient avant `chat.css` : `.messages { max-height: none }` du bureau est volontairement battu par le `max-height: 46dvh` de base.
- `telephone.css` vient après `file.css` et `chat.css` (il surcharge `.file`, `.chat`, `.messages`) ; `plein.css` vient en dernier.
- `.ilot` est défini deux fois : `ecran.css` (verre sur l'image), puis `commandes.css` (îlot des boutons), qui doit suivre.
- `.barre` fusionne la taille d'origine et l'ajustement ultérieur (20 px, centrée : la barre est au-dessus des îlots).
- `.haut` (titre dans le lecteur) est masqué par défaut dans `ecran.css` car l'information est déjà présente dans la barre de contrôle (`.barre-titre`), et ne s'affiche qu'en mode plein écran via `plein.css`.

Cadre : dans la coque (`:root.cadre`), l'en-tête flotte au-dessus de la vue ; le haut de page réserve `--haut-entete` au repos, permettant au contenu de remonter sous l'en-tête au défilement.
Mode studio : en mode studio (`.salle.cinema`), l'écran occupe toute la largeur de bord à bord au format 16:9 sans marges latérales. Le chat a une taille minimale alignée sur la playlist avec contenu (220 px) et s'étire en hauteur pour épouser la rangée. Sous l'écran, le layout est responsive : à partir de 1150 px, les présents passent à gauche de la file (3 colonnes : présents, file, chat), et en dessous de 1150 px la file et les présents s'empilent.
L'image reste sombre dans les deux thèmes, d'où les couleurs fixes (`--ecran-accent`) sur l'écran et les commandes.

Les styles des présents et des profils (`.present…`, `.menu-profil…`, `.badge-vocal`) sont regroupés dans les feuilles `presence-*` ;
ceux de `.presents` qui dépendent de la largeur (placement dans la grille de la scène) sont dans `presence-disposition.css`.
