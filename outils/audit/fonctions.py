import re

from longueurs import longueur_accolades, longueur_indentation

MOTS_CLES = r'(?:if|for|while|switch|catch|return|function)\b'
NOM = r'[A-Za-z_$][\w$]*'
RE_FONCTION = re.compile(r'^\s*(export\s+)?(default\s+)?(async\s+)?function\b\s*\*?\s*' + NOM + r'\s*[<(]')
RE_CONSTANTE = re.compile(
    r'^\s*(export\s+)?(const|let)\s+' + NOM + r'\s*(:[^=]+)?=\s*(async\s+)?'
    r'(?P<fonction>function\b|(<[^>]*>\s*)?(\(|' + NOM + r'\s*=>))'
)
RE_METHODE = re.compile(r'^\s+(async\s+)?(?!' + MOTS_CLES + r')' + NOM + r'\s*\([^)]*\)\s*(:\s*[^{]+)?\{\s*$')
RE_SHELL = re.compile(r'^\s*(?:function\s+)?[A-Za-z_][\w-]*\s*\(\)\s*\{')
RE_PYTHON = re.compile(r'^\s*(?:async\s+)?def\s+(\w+)')
MOTS_DECLARATION = {'export', 'default', 'async', 'function', 'const', 'let', 'def'}


def fleche_avant_fin(texte):
    profondeur = 0
    for i, caractere in enumerate(texte):
        if caractere in '([{':
            profondeur += 1
        elif caractere in ')]}':
            profondeur -= 1
        elif caractere == ';' and profondeur <= 0:
            return False
        elif texte[i:i + 2] == '=>':
            return True
    return False


def est_fonction(lignes, k, type_fichier):
    ligne = lignes[k]
    if type_fichier == 'sh':
        return bool(RE_SHELL.match(ligne))
    if type_fichier == 'py':
        return bool(RE_PYTHON.match(ligne))
    if RE_FONCTION.match(ligne) or RE_METHODE.match(ligne):
        return True
    constante = RE_CONSTANTE.match(ligne)
    if not constante:
        return False
    return bool(constante.group('fonction').startswith('function')
                or fleche_avant_fin('\n'.join(lignes[k:k + 8])))


def nom_fonction(ligne):
    for mot in re.findall(r'[A-Za-z_$][\w$]*', ligne):
        if mot not in MOTS_DECLARATION:
            return mot
    return '?'


def analyser_fonctions(masque, type_fichier):
    lignes = masque.split('\n')
    mesure = longueur_indentation if type_fichier == 'py' else longueur_accolades
    return [
        (nom_fonction(lignes[k]), mesure(lignes, k))
        for k in range(len(lignes)) if est_fonction(lignes, k, type_fichier)
    ]
