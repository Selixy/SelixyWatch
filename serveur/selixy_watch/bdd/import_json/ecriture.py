from selixy_watch.bdd.import_json import proprietaire
from selixy_watch.bdd.import_json.erreurs import ErreurImportJson
from selixy_watch.bdd.migrations import migrer


def verifier_vide(cx):
    for table in ("comptes", "noeuds"):
        if cx.execute(f"SELECT count(*) AS n FROM {table}").fetchone()["n"]:
            raise ErreurImportJson(f"La base contient déjà des données ({table}) : import refusé.")


def ecrire_comptes(cx, plan):
    for c in plan["comptes"]:
        cx.execute("INSERT INTO comptes (id, pseudo, pseudo_canonique, pseudo_squelette, avatar, avatar_version) VALUES (%s, %s, %s, %s, %s, %s)",
                   (c["id"], c["pseudo"], c["canonique"], c["squelette"], c["avatar"], c["version"]))
    for n in plan["noeuds"]:
        cx.execute("INSERT INTO noeuds (id, proprietaire_id, parent_id, type, nom, rang, cree_le) VALUES (%s, %s, %s, %s, %s, %s, to_timestamp(%s))",
                   (n["id"], n["proprietaire_id"], n["parent_id"], n["type"], n["nom"], n["rang"], n["t"]))


def ecrire_medias(cx, plan):
    for m in plan["medias"]:
        cx.execute("INSERT INTO medias (id, proprietaire_id, source, reference_youtube, nom, genre, duree, fichier, taille, miniature, cree_le)"
                   " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, to_timestamp(%s))",
                   (m["id"], m["proprietaire_id"], m["source"], m["reference_youtube"], m["nom"], m["genre"], m["duree"],
                    m["fichier"], m["taille"], m["miniature"], m["t"]))
    for playlist, media, rang in plan["pistes"]:
        cx.execute("INSERT INTO playlist_medias (playlist_id, media_id, rang) VALUES (%s, %s, %s)", (playlist, media, rang))


def ecrire_messages(cx, plan):
    for m in plan["messages"]:
        cx.execute("INSERT INTO messages (canal_id, compte_id, pseudo, texte, cree_le) VALUES (%s, %s, %s, %s, to_timestamp(%s))",
                   (m["canal_id"], m["compte_id"], m["pseudo"], m["texte"], m["t"]))


def appliquer(cx, plan):
    migrer(cx)
    verifier_vide(cx)
    ecrire_comptes(cx, plan)
    ecrire_medias(cx, plan)
    proprietaire.promouvoir(cx, plan)
    ecrire_messages(cx, plan)
