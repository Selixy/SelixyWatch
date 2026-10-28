export function descendants(noeuds, id) {
  const trouves = [];
  const pile = [id];
  while (pile.length) {
    const parent = pile.pop();
    for (const n of noeuds) if (n.parent === parent) { trouves.push(n.id); pile.push(n.id); }
  }
  return trouves;
}

export function couverts(noeuds, coches) {
  const ids = new Set();
  for (const id of coches) for (const d of descendants(noeuds, id)) ids.add(d);
  return ids;
}

export function hauts(noeuds, coches) {
  const sous = couverts(noeuds, coches);
  return [...coches].filter((id) => !sous.has(id));
}
