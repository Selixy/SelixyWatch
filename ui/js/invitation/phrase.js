function listeNoms(noms) {
  if (noms.length === 0) return 'un élément';
  if (noms.length === 1) return noms[0];
  if (noms.length === 2) return `${noms[0]} et ${noms[1]}`;
  const reste = noms.length - 2;
  return `${noms[0]}, ${noms[1]} et ${reste} autre${reste > 1 ? 's' : ''}`;
}

export const phrase = (inv) => `${inv.par?.pseudo || 'Quelqu\'un'} vous invite à ${listeNoms((inv.noeuds || []).map((n) => n.nom))}${inv.pro ? ' et vous offre le statut Pro' : ''}`;
