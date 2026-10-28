SELECTION_MOI = (
    "SELECT id, pseudo, avatar, avatar_version, quota_octets, ephemere, email, email_valide_le, email_en_attente, offre, admin, "
    "(SELECT COALESCE(SUM(taille), 0) FROM medias WHERE proprietaire_id = comptes.id) AS utilise FROM comptes WHERE id = %s"
)


def envoi_fichiers(ligne):
    return (ligne["offre"] == "pro" or ligne["admin"]) and ligne["email_valide_le"] is not None


def champs_courriel(ligne):
    return {
        "email": ligne["email"],
        "email_valide": ligne["email_valide_le"] is not None,
        "email_en_attente": ligne["email_en_attente"],
        "offre": ligne["offre"],
        "admin": ligne["admin"],
        "envoi_fichiers": envoi_fichiers(ligne),
    }
