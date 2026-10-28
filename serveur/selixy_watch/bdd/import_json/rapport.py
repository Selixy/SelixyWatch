def bloquants(plan):
    return bool(plan["invalides"] or plan["collisions"] or plan["erreurs"])


def lignes_blocages(plan):
    sortie = [f"PSEUDO INVALIDE {i} {p!r} : {m}" for i, p, m in plan["invalides"]]
    for groupe in plan["collisions"]:
        sortie.append("COLLISION (même pseudo ou pseudo trop ressemblant) : " + ", ".join(f"{p!r} ({i})" for i, p in groupe))
    return sortie + [f"ERREUR {e}" for e in plan["erreurs"]]


def lignes_alertes(plan):
    sortie = [f"Média orphelin (aucune playlist), ignoré : {m}" for m in plan["orphelins"]]
    sortie += [f"Piste vers un média absent de medias.json, ignorée : {m}" for m in plan["inconnus"]]
    sortie += [f"Fichier média manquant sur disque : {f}" for f in plan["manquants"]]
    if plan["messages_ignores"]:
        sortie.append(f"Messages ignorés (canal sans playlist) : {plan['messages_ignores']}")
    return sortie


def lignes_nombres(plan):
    return [f"{nom} : {len(plan[cle])}" for nom, cle in (("comptes", "comptes"), ("noeuds", "noeuds"), ("medias", "medias"),
                                                         ("playlist_medias", "pistes"), ("messages", "messages"))]


def texte(plan, applique):
    entete = "APPLIQUE" if applique else "SIMULATION (rien n'est écrit)"
    corps = lignes_nombres(plan) + lignes_blocages(plan) + lignes_alertes(plan)
    verdict = "REFUSE : résoudre les blocages ci-dessus (--renommer ancien=nouveau)." if bloquants(plan) else "Aucun blocage."
    return "\n".join([entete, *corps, verdict])
