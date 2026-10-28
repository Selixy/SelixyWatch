def effacer(sortie, debut, fin):
    for k in range(debut, fin):
        if sortie[k] != '\n':
            sortie[k] = ' '


def fin_chaine(texte, i):
    guillemet = texte[i]
    j = i + 1
    while j < len(texte) and texte[j] != guillemet and (guillemet == '`' or texte[j] != '\n'):
        j += 2 if texte[j] == '\\' else 1
    return min(j + 1, len(texte))


def debut_regex(texte, i):
    j = i - 1
    while j >= 0 and texte[j] in ' \t':
        j -= 1
    return j < 0 or texte[j] in '(,=:[!&|?{};+-*%<>~^\n' or texte[max(0, j - 5):j + 1] == 'return'


def fin_regex(texte, i):
    j = i + 1
    classe = False
    while j < len(texte) and texte[j] != '\n':
        k = texte[j]
        if k == '\\':
            j += 1
        elif k == '[':
            classe = True
        elif k == ']':
            classe = False
        elif k == '/' and not classe:
            return j + 1
        j += 1
    return -1


def passe(texte, mode):
    sortie = list(texte)
    taille = len(texte)
    i = 0
    total = 0
    while i < taille:
        k = texte[i]
        suivant = texte[i + 1:i + 2]
        if k in '\'"`':
            fin = fin_chaine(texte, i)
            effacer(sortie, i + 1, max(i + 1, fin - 1))
            i = fin
        elif k == '/' and suivant == '*':
            j = texte.find('*/', i + 2)
            fin = taille if j < 0 else j + 2
            effacer(sortie, i, fin)
            total += 1
            i = fin
        elif k == '/' and suivant == '/' and mode == 'ts':
            j = texte.find('\n', i)
            fin = taille if j < 0 else j
            effacer(sortie, i, fin)
            total += 1
            i = fin
        elif k == '/' and mode == 'ts' and debut_regex(texte, i) and fin_regex(texte, i) > 0:
            fin = fin_regex(texte, i)
            effacer(sortie, i + 1, fin - 1)
            i = fin
        else:
            i += 1
    return ''.join(sortie), total
