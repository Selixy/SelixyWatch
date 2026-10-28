SUITE_ATTENDUE = ('=>', '(', '=', ',', '&&', '||', '?', ':', '+', '<')


def longueur_accolades(lignes, k):
    profondeur = 0
    parentheses = 0
    vu = False
    for j in range(k, min(len(lignes), k + 3000)):
        for caractere in lignes[j]:
            if caractere in '([':
                parentheses += 1
            elif caractere in ')]':
                parentheses -= 1
            elif caractere == '{' and parentheses <= 0:
                profondeur += 1
                vu = True
            elif caractere == '}' and parentheses <= 0:
                profondeur -= 1
        if vu and profondeur <= 0:
            return j - k + 1
        if not vu and parentheses <= 0 and not lignes[j].rstrip().endswith(SUITE_ATTENDUE):
            return j - k + 1
    return 1


def longueur_indentation(lignes, k):
    base = len(lignes[k]) - len(lignes[k].lstrip())
    fin = k
    for j in range(k + 1, len(lignes)):
        if lignes[j].strip() == '':
            continue
        if len(lignes[j]) - len(lignes[j].lstrip()) <= base:
            break
        fin = j
    return fin - k + 1
