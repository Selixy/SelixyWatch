import os

from inventaire import lister_chemins

TYPES = {
    '.ts': 'ts', '.js': 'ts', '.mjs': 'ts', '.cjs': 'ts',
    '.vue': 'vue', '.sh': 'sh', '.py': 'py', '.css': 'css',
}
PREFIXES_EXCLUS = ('ui/visuels/',)
DOSSIERS_EXCLUS = ('node_modules', 'dist')


def type_mesure(chemin):
    base = os.path.basename(chemin)
    extension = os.path.splitext(base)[1]
    if base == 'Containerfile':
        return 'sh'
    return TYPES.get(extension)


def exclu(chemin):
    if chemin.startswith(PREFIXES_EXCLUS):
        return True
    return any(dossier in DOSSIERS_EXCLUS for dossier in chemin.split('/')[:-1])


def fichiers_mesures(racine):
    resultat = []
    for chemin in sorted(set(lister_chemins(racine))):
        type_fichier = type_mesure(chemin)
        if type_fichier and not exclu(chemin) and os.path.isfile(os.path.join(racine, chemin)):
            resultat.append((chemin, type_fichier))
    return resultat
