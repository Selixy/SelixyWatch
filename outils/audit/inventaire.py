import os
import subprocess

DOSSIERS_IGNORES = ('.git', 'node_modules', 'dist')


def racine_de_depot(racine):
    resultat = subprocess.run(
        ['git', 'rev-parse', '--show-toplevel'],
        cwd=racine, capture_output=True, text=True,
    )
    if resultat.returncode != 0:
        return False
    return os.path.realpath(resultat.stdout.strip()) == os.path.realpath(racine)


def chemins_suivis(racine):
    return subprocess.run(
        ['git', 'ls-files', '-co', '--exclude-standard'],
        cwd=racine, capture_output=True, text=True, check=True,
    ).stdout.splitlines()


def chemins_de_l_arbre(racine):
    chemins = []
    for dossier, sous_dossiers, fichiers in os.walk(racine):
        sous_dossiers[:] = [nom for nom in sous_dossiers if nom not in DOSSIERS_IGNORES]
        relatif = os.path.relpath(dossier, racine)
        for nom in fichiers:
            chemins.append(nom if relatif == '.' else f'{relatif}/{nom}')
    return chemins


def lister_chemins(racine):
    if racine_de_depot(racine):
        return chemins_suivis(racine)
    return chemins_de_l_arbre(racine)
