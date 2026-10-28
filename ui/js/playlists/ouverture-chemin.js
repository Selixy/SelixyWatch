export function idsADeplier(n, noeud) {
  const ids = n.type === 'dossier' ? [n.id] : [];
  for (let p = noeud(n.parent); p; p = noeud(p.parent)) ids.push(p.id);
  return ids;
}
