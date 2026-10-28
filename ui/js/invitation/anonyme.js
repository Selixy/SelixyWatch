export const AVERTISSEMENT = 'Compte anonyme : tout ce que vous créez sera supprimé à la déconnexion.';

export async function creerAnonyme(api) {
  const r = await api('/api/anonyme', { method: 'POST' });
  if (r.ok) return { profil: r.data };
  return { erreur: r.data?.erreur || r.data?.message || 'Entrée en anonyme impossible.' };
}

export const confirmerDeconnexion = (profil, confirmer) => !profil?.ephemere
  || confirmer(`${AVERTISSEMENT} Se déconnecter quand même ?`);
