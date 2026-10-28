import os
import subprocess

SCRIPT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'banc-bdd.sh')


def ouvrir_base():
    fournie = os.environ.get('BDD_URL')
    if fournie:
        return fournie, False
    sortie = subprocess.run(['bash', SCRIPT, 'demarrer'], check=True, capture_output=True, text=True)
    return sortie.stdout.strip().splitlines()[-1], True


def fermer_base(lancee):
    if lancee:
        subprocess.run(['bash', SCRIPT, 'arreter'], check=False)
