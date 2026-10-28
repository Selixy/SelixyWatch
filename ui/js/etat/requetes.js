import { api } from '../api.js';

export async function poster(url, corps) {
  const r = await api(url, { method: 'POST', body: corps });
  if (!r.ok) throw new Error(r.data?.erreur || 'Erreur de communication avec le serveur.');
  return r.data;
}

export const actionPlaylist = (id, nomAction, corps = {}) => poster(`/api/playlist/${id}/${nomAction}`, corps);
export const actionArbre = (nomAction, corps = {}) => poster(`/api/arbre/${nomAction}`, corps);
