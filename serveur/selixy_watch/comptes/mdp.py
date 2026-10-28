import base64
import hashlib
import hmac
import secrets

from selixy_watch.erreurs import Refus

COUT_N = 2**14
COUT_R = 8
COUT_P = 1
TAILLE_SEL = 16
MDP_MIN = 8
MDP_MAX = 128


def derive(mdp, sel, n, r, p):
    return hashlib.scrypt(mdp.encode(), salt=sel, n=n, r=r, p=p, dklen=32)


def hacher(mdp):
    sel = secrets.token_bytes(TAILLE_SEL)
    sel64 = base64.b64encode(sel).decode()
    hash64 = base64.b64encode(derive(mdp, sel, COUT_N, COUT_R, COUT_P)).decode()
    return f"scrypt${COUT_N}${COUT_R}${COUT_P}${sel64}${hash64}"


def verifier(mdp, empreinte):
    try:
        marque, n, r, p, sel, attendu = empreinte.split("$")
        calcule = derive(mdp, base64.b64decode(sel), int(n), int(r), int(p))
        return marque == "scrypt" and hmac.compare_digest(calcule, base64.b64decode(attendu))
    except ValueError:
        return False


def valider_mdp(mdp):
    if not isinstance(mdp, str) or not MDP_MIN <= len(mdp) <= MDP_MAX:
        raise Refus(400, f"Le mot de passe doit faire de {MDP_MIN} à {MDP_MAX} caractères.")
    return mdp


EMPREINTE_LEURRE = hacher("leurre-sans-compte")
