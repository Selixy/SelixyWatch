const TEXTES = {
  401: 'Connectez-vous pour accepter cette invitation.',
  404: 'Cette invitation n\'existe pas ou n\'existe plus.',
  410: 'Cette invitation a expiré ou n\'a plus de place.',
};

export const texteErreur = (statut, donnees) => TEXTES[statut] || donnees?.erreur || 'Invitation impossible à traiter.';

export async function voir(api, jeton) {
  const r = await api('/api/invitation/voir', { method: 'POST', body: { jeton } });
  return r.ok ? { invitation: r.data } : { erreur: texteErreur(r.status, r.data) };
}

export async function accepter(api, jeton) {
  const r = await api('/api/invitation/accepter', { method: 'POST', body: { jeton } });
  return r.ok ? { noeuds: r.data.noeuds || [], deja: !!r.data.deja } : { erreur: texteErreur(r.status, r.data) };
}
