from selixy_watch.comptes import profils
from selixy_watch.configuration import MAX_CHAT


def forme_message(ligne, auteur):
    return {"id": str(ligne["id"]), "t": ligne["cree_le"].timestamp(), "auteur": auteur, "texte": ligne["texte"]}


def enregistrer(cx, canal, auteur, texte):
    ligne = cx.execute(
        "INSERT INTO messages (canal_id, compte_id, pseudo, texte) VALUES (%s, %s, %s, %s) RETURNING id, cree_le, texte",
        (canal, auteur["id"], auteur["pseudo"], texte),
    ).fetchone()
    return forme_message(ligne, auteur)


def derniers(cx, canal):
    lignes = cx.execute(
        "SELECT id, compte_id, pseudo, texte, cree_le FROM messages WHERE canal_id = %s ORDER BY id DESC LIMIT %s",
        (canal, MAX_CHAT),
    ).fetchall()
    connus = profils.publics(cx, {ligne["compte_id"] for ligne in lignes if ligne["compte_id"]})
    anonyme = lambda ligne: {"id": None, "pseudo": ligne["pseudo"], "avatar": None}
    return [forme_message(ligne, connus.get(ligne["compte_id"]) or anonyme(ligne)) for ligne in reversed(lignes)]
