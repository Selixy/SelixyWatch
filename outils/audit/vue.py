import re

RE_BLOC = re.compile(r'<(script|style)\b[^>]*>(.*?)</\1>', re.S)
RE_STYLE = re.compile(r'^[ \t]*<style\b.*?</style>[^\n]*\n?', re.S | re.M)


def decouper_vue(texte):
    blocs = {'script': '', 'style': ''}
    for nom, contenu in RE_BLOC.findall(texte):
        blocs[nom] += contenu
    gabarit = RE_BLOC.sub('', texte)
    nombre_lignes = len(RE_STYLE.sub('', texte).splitlines())
    return blocs['script'], gabarit, blocs['style'], nombre_lignes
