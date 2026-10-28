import re

TAILLE_BLOC = 10 * 1024 * 1024
MOTIF = re.compile(r'bytes=(\d*)-(\d*)')


def plage_amont(entete):
    trouve = MOTIF.fullmatch((entete or '').strip())
    if not trouve or not trouve.group(1):
        return f'bytes=0-{TAILLE_BLOC - 1}'
    debut = int(trouve.group(1))
    plafond = debut + TAILLE_BLOC - 1
    fin = min(int(trouve.group(2)), plafond) if trouve.group(2) else plafond
    return f'bytes={debut}-{fin}'
