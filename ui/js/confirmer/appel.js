const TEXTES = {
  409: 'Cette adresse est déjà validée par un autre compte.',
  410: 'Ce lien a expiré ou a déjà été utilisé. Demandez-en un nouveau depuis votre profil.',
};

export const texteConfirmation = (statut, donnees) => TEXTES[statut] || donnees?.erreur || 'Confirmation impossible.';

export async function confirmer(api, jeton) {
  const r = await api('/api/email/confirmer', { method: 'POST', body: { jeton } });
  return r.ok ? { email: r.data?.email } : { erreur: texteConfirmation(r.status, r.data) };
}
