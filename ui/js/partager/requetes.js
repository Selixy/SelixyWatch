import { api } from '../api.js';
import { poster } from '../etat.js';

export const actionPartage = (id, nom, corps = {}) => poster(`/api/partage/${id}/${nom}`, corps);

export async function lirePartage(id) {
  const r = await api(`/api/partage?noeud=${encodeURIComponent(id)}`);
  if (!r.ok) throw new Error(r.data?.erreur || 'Partage illisible.');
  return r.data;
}
