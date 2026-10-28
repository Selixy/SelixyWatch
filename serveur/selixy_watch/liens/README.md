# liens

Import de liens YouTube et Spotify dans une playlist (`POST /api/liens {url, playlist}`, 202, import en arrière-plan).

- La route exige un compte connecté ayant le droit « editeur » sur la playlist ; le compte est passé à `importer` puis à `SuiviImport`.
- Chaque vidéo devient un média dédoublonné par (propriétaire, référence YouTube) qui appartient au compte qui importe
  (`playlist.ajout_youtube`).
- `SuiviImport.publier` (tous les 5 ajouts ou chaque seconde) appelle `canaux.synchro.playlist_modifiee` et signale les comptes concernés,
  pour que la playlist se remplisse à vue. Si la playlist a disparu entre-temps, rien n'est publié.
- Le nombre d'imports simultanés (2) est limité par `etat.imports`. L'événement SSE `import` reste diffusé à tous les abonnés.
