import { noeud, estPlaylist } from './arbre.js';

export const nom = (id) => (id === 'racine' ? 'Bibliothèque' : noeud(id)?.nom ?? '');
export const ordre = (canal) => (estPlaylist(canal) ? noeud(canal).pistes : []);

export function chemin(id) {
  const noms = [];
  for (let n = noeud(id); n && noms.length < 12; n = noeud(n.parent)) noms.unshift(n.nom);
  return noms.join(' › ');
}
