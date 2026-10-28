import os

DOSSIERS_ADMIS = ('heritage/', 'dormant/')


def lire_exceptions(chemin):
    exceptions = {}
    if not os.path.exists(chemin):
        return exceptions
    with open(chemin, encoding='utf-8') as flux:
        for ligne in flux:
            champs = ligne.split()
            if champs:
                exceptions[champs[0]] = set(champs[1].split(',')) if len(champs) > 1 else set()
    return exceptions


def permis_pour(chemin, exceptions):
    if chemin in exceptions:
        return exceptions[chemin]
    for dossier in DOSSIERS_ADMIS:
        if chemin.startswith(dossier) and exceptions.get(dossier) == {'*'}:
            return {'*'}
    return set()


def exceptions_perimees(ecarts, mesures, exceptions):
    sorties = []
    for entree, noms in sorted(exceptions.items()):
        if entree.endswith('/'):
            if entree not in DOSSIERS_ADMIS or noms != {'*'}:
                sorties.append(f'EXCEPTION INVALIDE {entree} : dossier entier reserve a heritage/ et dormant/')
            elif not any(chemin.startswith(entree) for chemin in ecarts):
                sorties.append(f'EXCEPTION PERIMEE {entree} : aucun ecart (retirer de la liste)')
        elif entree not in mesures:
            sorties.append(f'EXCEPTION PERIMEE {entree} : fichier absent (retirer de la liste)')
        else:
            for nom in sorted(noms - set(ecarts.get(entree, {}))):
                sorties.append(f'EXCEPTION PERIMEE {entree} : {nom} (retirer de la liste)')
    return sorties


def confronter(ecarts, mesures, exceptions):
    sorties = []
    couverts = 0
    for chemin, details in sorted(ecarts.items()):
        permis = permis_pour(chemin, exceptions)
        restants = {nom: d for nom, d in details.items() if nom not in permis and '*' not in permis}
        couverts += len(details) - len(restants)
        if restants:
            sorties.append(f'ECART {chemin} : ' + ' '.join(f'{nom}={d}' for nom, d in restants.items()))
    return sorties + exceptions_perimees(ecarts, mesures, exceptions), couverts
