from selixy_watch.acces import droits
from selixy_watch.bibliotheque import lecture
from selixy_watch.bibliotheque.champs import identifiant, identifiant_facultatif
from selixy_watch.bibliotheque.ecriture import ecriture
from selixy_watch.canaux import synchro
from selixy_watch.diffusion.bibliotheque import signaler
from selixy_watch.erreurs import Refus
from selixy_watch.playlist import pistes

ACTIONS = {"ajouter": pistes.ajouter, "retirer": pistes.retirer, "deplacer": pistes.deplacer}


def action_playlist(ident, pid, action, d):
    traitement = ACTIONS.get(action)
    if traitement is None:
        raise Refus(404, "action inconnue")
    mid = identifiant(d.get("media"), "média inconnu")
    avant = identifiant_facultatif(d.get("avant"))
    with ecriture() as cx:
        droits.exiger(cx, ident, pid, "editeur")
        if not lecture.est_playlist(cx, pid):
            raise Refus(404, "playlist inconnue")
        concernes = droits.concernes(cx, pid)
        traitement(cx, ident, pid, mid, avant)
        synchro.playlist_modifiee(cx, pid)
    signaler(concernes)
    return {"ok": 1}
