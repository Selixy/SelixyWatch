export const texteRecuperation = (statut, donnees) => (statut === 410
  ? 'Ce lien a expiré ou a déjà été utilisé. Demandez-en un nouveau depuis la page de connexion.'
  : donnees?.erreur || 'Changement impossible.');

export async function renouveler(api, jeton, mdp) {
  const r = await api('/api/recuperation/mdp', { method: 'POST', body: { jeton, mdp } });
  return r.ok ? {} : { erreur: texteRecuperation(r.status, r.data) };
}
