export const estMien = (n) => !!n && n.role === 'proprietaire';
export const mesNoeuds = (noeuds) => noeuds.filter(estMien);

export function basculer(coches, id, coche) {
  const suivant = new Set(coches);
  if (coche) suivant.add(id); else suivant.delete(id);
  return suivant;
}
