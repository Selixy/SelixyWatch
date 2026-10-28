# medias

Envoi de fichiers et miniatures. `POST /api/medias` (corps brut, en-têtes `X-Nom`, `X-Duree`, `X-Playlist`) et
`POST /api/medias/<id>/miniature` (jpeg, 200 Ko).

- `reception.py` : lecture du flux et écriture du fichier ; `description.py` : nom et durée à partir des en-têtes ; `enregistrement.py` :
  insertion en base et ajout en fin de playlist ; `quota.py` : espace utilisé et quota du compte.
- Le média appartient à l'expéditeur, même s'il envoie dans la playlist de quelqu'un d'autre (droit « editeur » requis). Quota par compte :
  somme des `taille` de ses médias plus l'envoi au plus `quota_octets` (507). 4 Go au plus par fichier (413).
- Le quota est vérifié avant la lecture du corps (rejet rapide) et de nouveau à l'insertion (deux envois simultanés). Si l'insertion échoue,
  le fichier écrit est supprimé.
- Miniature : réservée au propriétaire du média (404 sinon) ; les comptes qui voient le média sont signalés.
