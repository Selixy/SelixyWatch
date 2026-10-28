import os
import sys

from ecarts import calculer_ecarts
from exceptions import confronter, lire_exceptions
from perimetre import fichiers_mesures


def lire_racine(arguments):
    defaut = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
    if arguments[:1] == ['--racine'] and len(arguments) == 2:
        return os.path.abspath(arguments[1])
    if arguments:
        sys.exit('usage : audit-modulaire.sh [--racine DIR]')
    return defaut


def main(arguments):
    racine = lire_racine(arguments)
    fichiers = fichiers_mesures(racine)
    ecarts = {}
    for chemin, type_fichier in fichiers:
        trouves = calculer_ecarts(racine, chemin, type_fichier)
        if trouves:
            ecarts[chemin] = trouves
    exceptions = lire_exceptions(os.path.join(racine, 'outils', 'audit-exceptions.txt'))
    sorties, couverts = confronter(ecarts, {chemin for chemin, _ in fichiers}, exceptions)
    for ligne in sorties:
        print(ligne)
    print(f'audit modulaire : {len(fichiers)} fichiers, {len(sorties)} ecart(s), {couverts} ecart(s) sous exception')
    return 1 if sorties else 0


sys.exit(main(sys.argv[1:]))
