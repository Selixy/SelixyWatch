import argparse
import getpass

from selixy_watch.bdd.import_json import ecriture, lecture, plan as plan_import, rapport
from selixy_watch.bdd.import_json.erreurs import ErreurImportJson
from selixy_watch.comptes.mdp import hacher, valider_mdp
from selixy_watch.erreurs import Refus


def renommage(texte):
    ancien, separateur, nouveau = texte.partition("=")
    if not separateur or not ancien or not nouveau:
        raise argparse.ArgumentTypeError("attendu : ancien=nouveau")
    return ancien, nouveau


def lire_arguments(argv):
    p = argparse.ArgumentParser(prog="importer_json.py", description="Importe les données JSON de production dans PostgreSQL.")
    p.add_argument("--dossier", required=True)
    p.add_argument("--proprietaire", required=True)
    p.add_argument("--renommer", action="append", default=[], type=renommage, metavar="ancien=nouveau")
    p.add_argument("--appliquer", action="store_true")
    p.add_argument("--definir-mdp", action="store_true", help="demande le mot de passe du propriétaire (saisie masquée)")
    return p.parse_args(argv)


def demander_mdp():
    mdp = getpass.getpass("Mot de passe du propriétaire : ")
    if mdp != getpass.getpass("Confirmation : "):
        raise ErreurImportJson("Les deux mots de passe diffèrent.")
    try:
        valider_mdp(mdp)
    except Refus as e:
        raise ErreurImportJson(e.message)
    return mdp


def definir_mdp(cx, compte, mdp):
    cx.execute("UPDATE comptes SET mdp_hash = %s WHERE id = %s", (hacher(mdp), compte))


def executer(argv, transaction, saisir_mdp=demander_mdp):
    args = lire_arguments(argv)
    try:
        calcule = plan_import.construire(lecture.lire_dossier(args.dossier), args.proprietaire, dict(args.renommer), args.dossier)
        refuse = args.appliquer and rapport.bloquants(calcule)
        if args.appliquer and not refuse:
            mdp = saisir_mdp() if args.definir_mdp else None
            with transaction() as cx:
                ecriture.appliquer(cx, calcule)
                if mdp:
                    definir_mdp(cx, calcule["proprietaire"], mdp)
    except ErreurImportJson as e:
        return 1, f"ERREUR {e}"
    return (1 if refuse else 0), rapport.texte(calcule, args.appliquer and not refuse)
