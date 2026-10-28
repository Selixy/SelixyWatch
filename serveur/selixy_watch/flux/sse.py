import json
import queue
import urllib.parse

from selixy_watch.acces.droits import role_sur
from selixy_watch.bdd.connexion import transaction
from selixy_watch.bibliotheque.lecture import est_playlist
from selixy_watch.canaux.occupation import auto_demarrer, auto_mettre_en_pause, canal_occupe
from selixy_watch.comptes.session import ident
from selixy_watch.diffusion.presence import diffuser_presence
from selixy_watch.etat import ABONNES, verrou
from selixy_watch.flux.depart import evenements_de_depart
from selixy_watch.vocal.etats import quitter_vocal


def ecrire_evenement(h, nom, donnees):
    h.wfile.write(f"event: {nom}\ndata: {json.dumps(donnees, ensure_ascii=False)}\n\n".encode())
    h.wfile.flush()


def servir_evenements(h, q, depart):
    for nom, donnees in depart:
        ecrire_evenement(h, nom, donnees)
    while True:
        try:
            evenement, donnees = q.get(timeout=15)
            ecrire_evenement(h, evenement, donnees)
        except queue.Empty:
            h.wfile.write(b": ping\n\n")
            h.wfile.flush()


def servir_flux(h, canal):
    q = queue.Queue(maxsize=300)
    h.send_response(200)
    h.send_header("Content-Type", "text/event-stream; charset=utf-8")
    h.send_header("Cache-Control", "no-cache")
    h.send_header("X-Accel-Buffering", "no")
    h.end_headers()
    compte = ident(h)
    with verrou, transaction() as cx:
        occupe = canal_occupe(canal) if canal else True
        ABONNES[q] = {"canal": canal, "ident": compte}
        if canal and not occupe:
            auto_demarrer(cx, canal)
        depart = evenements_de_depart(cx, canal, compte)
        diffuser_presence()
    try:
        servir_evenements(h, q, depart)
    except (BrokenPipeError, ConnectionResetError, OSError):
        pass
    finally:
        with verrou, transaction() as cx:
            ABONNES.pop(q, None)
            if canal and compte:
                quitter_vocal(canal, compte)
            auto_mettre_en_pause(cx, canal)
            diffuser_presence()


def route_flux(h, url):
    canal = urllib.parse.parse_qs(url.query).get("canal", [""])[0]
    with transaction() as cx:
        autorise = bool(canal) and est_playlist(cx, canal) and role_sur(cx, ident(h), canal) is not None
    servir_flux(h, canal if autorise else None)


ROUTES_GET = {"/api/flux": route_flux}
