from selixy_watch.comptes.pseudo import canonique

GO = 1024 ** 3
QUOTA_PRO_PAR_DEFAUT_GO = 20


class ErreurAdministration(Exception):
    pass


def trouver(cx, pseudo):
    ligne = cx.execute(
        "SELECT id, pseudo, email_valide_le FROM comptes WHERE pseudo_canonique = %s AND NOT ephemere", (canonique(pseudo),)
    ).fetchone()
    if not ligne:
        raise ErreurAdministration(f"Compte introuvable : {pseudo}")
    return ligne


def passer_pro(cx, pseudo, quota_go=QUOTA_PRO_PAR_DEFAUT_GO):
    compte = trouver(cx, pseudo)
    if compte["email_valide_le"] is None:
        raise ErreurAdministration(f"{compte['pseudo']} n'a pas d'adresse e-mail validée : offre Pro refusée.")
    cx.execute("UPDATE comptes SET offre = 'pro', quota_octets = %s WHERE id = %s", (int(quota_go * GO), compte["id"]))
    return f"{compte['pseudo']} : offre Pro, quota {quota_go} Go."


def passer_free(cx, pseudo):
    compte = trouver(cx, pseudo)
    cx.execute("UPDATE comptes SET offre = 'free', quota_octets = 0 WHERE id = %s", (compte["id"],))
    return f"{compte['pseudo']} : offre Free (les fichiers existants restent, l'envoi est bloqué)."


def fixer_quota(cx, pseudo, quota_go):
    compte = trouver(cx, pseudo)
    cx.execute("UPDATE comptes SET quota_octets = %s WHERE id = %s", (int(quota_go * GO), compte["id"]))
    return f"{compte['pseudo']} : quota {quota_go} Go."


def lister(cx):
    lignes = cx.execute(
        "SELECT pseudo, offre, admin, email_valide_le IS NOT NULL AS valide, quota_octets, "
        "(SELECT COALESCE(SUM(taille), 0) FROM medias WHERE proprietaire_id = comptes.id) AS utilise "
        "FROM comptes WHERE NOT ephemere ORDER BY pseudo_canonique"
    ).fetchall()
    return "\n".join(
        f"{c['pseudo']}\t{c['offre']}{' admin' if c['admin'] else ''}\te-mail {'validé' if c['valide'] else 'non validé'}\t{int(c['utilise']) / GO:.2f} / {c['quota_octets'] / GO:.2f} Go"
        for c in lignes
    ) or "Aucun compte."
