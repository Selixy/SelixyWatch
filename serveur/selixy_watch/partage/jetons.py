import hashlib
import secrets


def hacher(jeton):
    return hashlib.sha256(jeton.encode()).hexdigest()


def nouveau():
    jeton = secrets.token_urlsafe(24)
    return jeton, hacher(jeton), secrets.token_hex(6)
