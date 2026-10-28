import os


def url_publique():
    return os.environ.get("URL_PUBLIQUE", "https://watch.selixy.dev").rstrip("/")


def confirmation(jeton):
    lien = f"{url_publique()}/confirmer/#{jeton}"
    texte = (
        "Bonjour,\n\n"
        "Pour confirmer cette adresse sur SelixyWatch, ouvrez ce lien (valable 24 heures) :\n\n"
        f"{lien}\n\n"
        "Si vous n'êtes pas à l'origine de cette demande, ignorez ce message.\n"
    )
    return "Confirmez votre adresse e-mail", texte


def recuperation(jeton):
    lien = f"{url_publique()}/recuperation/#{jeton}"
    texte = (
        "Bonjour,\n\n"
        "Pour choisir un nouveau mot de passe sur SelixyWatch, ouvrez ce lien (valable 1 heure, une seule fois) :\n\n"
        f"{lien}\n\n"
        "Si vous n'avez rien demandé, ignorez ce message : votre mot de passe reste inchangé.\n"
    )
    return "Récupération de votre compte", texte
