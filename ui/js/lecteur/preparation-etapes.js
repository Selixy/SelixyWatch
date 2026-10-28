export const DELAI_MS = 600;
export const ABANDON_MS = 20000;

export function decider(p, prete, maintenant) {
  if (p.fini) return 'rien';
  if (prete) return p.pose ? 'retirer' : 'terminer';
  if (!p.debut) return 'demarrer';
  if (maintenant - p.debut >= ABANDON_MS) return p.pose ? 'retirer' : 'terminer';
  return !p.pose && maintenant - p.debut >= DELAI_MS ? 'poser' : 'attendre';
}

export function lecteurEstPret(lecteur, bloque) {
  return bloque || (lecteur.preparee ? lecteur.preparee() : lecteur.pret());
}
