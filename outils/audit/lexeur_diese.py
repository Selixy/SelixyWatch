import re

from lexeur_c import effacer, fin_chaine

RE_HEREDOC = re.compile(r'(?<!<)<<(?!<)-?\s*[\'"]?([A-Za-z_]\w*)[\'"]?')


def balayer_ligne_shell(ligne, guillemet):
    sortie = []
    i = 0
    while i < len(ligne):
        k = ligne[i]
        suivant = ligne[i + 1:i + 2]
        pas = 1
        if guillemet:
            if k == '\\' and guillemet == '"':
                sortie.append('  ')
                pas = 2
            elif k == guillemet:
                sortie.append(k)
                guillemet = ''
            else:
                sortie.append(' ')
        elif k in '\'"':
            guillemet = k
            sortie.append(k)
        elif k == '\\':
            sortie.append('  ')
            pas = 2
        elif k == '$' and suivant in ('#', '{'):
            sortie.append('$ ' if suivant == '#' else '${')
            pas = 2
        elif k == '#' and (i == 0 or ligne[i - 1] in ' \t;|&('):
            return ''.join(sortie), True, guillemet
        else:
            sortie.append(k)
        i += pas
    return ''.join(sortie), False, guillemet


def masquer_shell(texte):
    sortie = []
    heredoc = ''
    guillemet = ''
    total = 0
    for numero, ligne in enumerate(texte.split('\n')):
        if heredoc:
            heredoc = '' if ligne.strip() == heredoc else heredoc
            sortie.append('')
            continue
        masque, commentaire, guillemet = balayer_ligne_shell(ligne, guillemet)
        if commentaire and not (numero == 0 and ligne.startswith('#!')):
            total += 1
        trouve = RE_HEREDOC.search(ligne) if not guillemet and not commentaire else None
        heredoc = trouve.group(1) if trouve else ''
        sortie.append(masque)
    return '\n'.join(sortie), total


def est_docstring(texte, i):
    debut = texte.rfind('\n', 0, i) + 1
    if texte[debut:i].strip():
        return False
    avant = texte[:debut].rstrip()
    return not avant or avant[-1] not in '(,=[\\{'


def masquer_python(texte):
    sortie = list(texte)
    taille = len(texte)
    i = 0
    total = 0
    while i < taille:
        k = texte[i]
        triple = texte[i:i + 3]
        if k == '#':
            j = texte.find('\n', i)
            fin = taille if j < 0 else j
            total += 0 if i == 0 and texte.startswith('#!') else 1
            effacer(sortie, i, fin)
            i = fin
        elif triple in ('"""', "'''"):
            j = texte.find(triple, i + 3)
            fin = taille if j < 0 else j + 3
            total += 1 if est_docstring(texte, i) else 0
            effacer(sortie, i + 3, max(i + 3, fin - 3))
            i = fin
        elif k in '\'"':
            fin = fin_chaine(texte, i)
            effacer(sortie, i + 1, max(i + 1, fin - 1))
            i = fin
        else:
            i += 1
    return ''.join(sortie), total
