import argparse

from selixy_watch.administration import commandes, statut_admin


def lire_arguments(argv):
    p = argparse.ArgumentParser(prog="administrer.py", description="Administration des comptes SelixyWatch (base : BDD_URL).")
    sous = p.add_subparsers(dest="commande", required=True)
    pro = sous.add_parser("pro", help="attribue l'offre Pro (e-mail validé requis)")
    pro.add_argument("pseudo")
    pro.add_argument("--quota-go", type=float, default=commandes.QUOTA_PRO_PAR_DEFAUT_GO)
    sous.add_parser("free", help="repasse en Free (quota 0, fichiers conservés)").add_argument("pseudo")
    quota = sous.add_parser("quota", help="fixe le quota en Go")
    quota.add_argument("pseudo")
    quota.add_argument("go", type=float)
    sous.add_parser("admin", help="donne le statut d'administrateur (Pro illimité)").add_argument("pseudo")
    sous.add_parser("retirer-admin", help="retire le statut d'administrateur").add_argument("pseudo")
    sous.add_parser("lister", help="liste les comptes, offres et quotas")
    return p.parse_args(argv)


def appliquer(cx, args):
    if args.commande == "pro":
        return commandes.passer_pro(cx, args.pseudo, args.quota_go)
    if args.commande == "free":
        return commandes.passer_free(cx, args.pseudo)
    if args.commande == "quota":
        return commandes.fixer_quota(cx, args.pseudo, args.go)
    if args.commande in ("admin", "retirer-admin"):
        return statut_admin.definir_admin(cx, args.pseudo, args.commande == "admin")
    return commandes.lister(cx)


def executer(argv, transaction):
    args = lire_arguments(argv)
    try:
        with transaction() as cx:
            return 0, appliquer(cx, args)
    except commandes.ErreurAdministration as erreur:
        return 1, f"ERREUR {erreur}"
