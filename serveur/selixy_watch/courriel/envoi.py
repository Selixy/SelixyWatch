import os
import sys
import urllib.request
from datetime import datetime, timezone
from email.message import EmailMessage
from email.policy import SMTP
from email.utils import format_datetime, make_msgid

EXPEDITEUR = "SelixyWatch <watch@selixy.dev>"
ADRESSE_EXPEDITEUR = "watch@selixy.dev"
BOITE_MEMOIRE = []


def lire_secret():
    chemin = os.environ.get("MAIL_SECRET_FICHIER", "/secrets/mail_secret.txt")
    with open(chemin, encoding="utf-8") as f:
        return f.read().strip()


def construire(destinataire, sujet, texte):
    message = EmailMessage(policy=SMTP)
    message["From"] = EXPEDITEUR
    message["To"] = destinataire
    message["Subject"] = sujet
    message["Date"] = format_datetime(datetime.now(timezone.utc))
    message["Message-ID"] = make_msgid(domain="selixy.dev")
    message.set_content(texte, charset="utf-8")
    return message


def poster(url, brut, destinataire):
    requete = urllib.request.Request(url, data=brut, method="POST", headers={
        "Authorization": "Bearer " + lire_secret(),
        "X-To": destinataire,
        "X-From": ADRESSE_EXPEDITEUR,
        "Content-Type": "message/rfc822",
    })
    with urllib.request.urlopen(requete, timeout=10) as reponse:
        if reponse.status >= 300:
            raise RuntimeError(f"réponse {reponse.status}")


def envoyer(destinataire, sujet, texte):
    url = os.environ.get("MAIL_URL", "stdout")
    try:
        if url == "memoire":
            BOITE_MEMOIRE.append({"destinataire": destinataire, "sujet": sujet, "texte": texte})
        elif url == "stdout":
            print(f"--- courriel à {destinataire} : {sujet}\n{texte}\n---", flush=True)
        else:
            poster(url, construire(destinataire, sujet, texte).as_bytes(), destinataire)
        return True
    except Exception as erreur:
        print(f"courriel : échec d'envoi ({sujet}) : {erreur}", file=sys.stderr, flush=True)
        return False
