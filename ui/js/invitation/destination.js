export const CLE_CANAL = 'mu-canal';
export const CLE_DOSSIER = 'mu-dossier';

export const destination = (noeud) => (noeud?.type === 'playlist'
  ? { vue: 'room', cle: CLE_CANAL, id: noeud.id }
  : { vue: 'playlists', cle: CLE_DOSSIER, id: noeud?.id });

export const destinationDe = (noeuds) => (noeuds.length === 1
  ? destination(noeuds[0])
  : { vue: 'playlists', cle: CLE_DOSSIER, id: noeuds[0]?.id });

export function entrerDans(noeuds, { stockage, cadre, parent, aller }) {
  const d = destinationDe(noeuds);
  try { stockage.setItem(d.cle, d.id); } catch { return; }
  if (!cadre) return aller('/#' + d.vue);
  if (d.vue === 'room') parent.postMessage({ type: 'entrer', id: d.id }, '*');
  else parent.postMessage({ type: 'recharger', vue: d.vue }, '*');
}
