from selixy_watch.administration.commandes import GO, QUOTA_PRO_PAR_DEFAUT_GO


def promouvoir(cx, plan):
    cx.execute(
        "UPDATE comptes SET offre = 'pro', admin = true, quota_octets = GREATEST(%s::bigint, "
        "(SELECT COALESCE(SUM(taille), 0) FROM medias WHERE proprietaire_id = comptes.id)) WHERE id = %s",
        (QUOTA_PRO_PAR_DEFAUT_GO * GO, plan["proprietaire"]),
    )
