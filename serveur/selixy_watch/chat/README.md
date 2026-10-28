# chat

Messages en base (table `messages`, supprimés avec la playlist). `historique.derniers` renvoie les `MAX_CHAT` (100) derniers, du plus
ancien au plus récent, même forme qu'avant : `id` (texte), `t` (secondes epoch), `auteur` public, `texte`. Le pseudo est copié dans la ligne :
si le compte est supprimé (`compte_id` NULL), le message reste avec son pseudo et un auteur sans identifiant ni avatar.

Écrire ou réagir exige le rôle lecteur sur la playlist (`canaux.acces_salle`). La limite de débit reste en mémoire.
`historique` appelle `comptes.profils.publics` par le module, pour que la fonction soit résolue à l'appel.
