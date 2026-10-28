const FORME = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export function etatEmail(profil) {
  if (profil?.email_valide && profil.email) return { mode: 'valide', adresse: profil.email, texte: `Adresse validée : ${profil.email}` };
  if (profil?.email_en_attente) return { mode: 'attente', adresse: profil.email_en_attente, texte: `En attente de validation : ${profil.email_en_attente}` };
  return { mode: 'aucun', adresse: '', texte: 'Facultative : elle sert à récupérer votre compte si vous oubliez le mot de passe.' };
}

export function erreurEmail(adresse, mdp) {
  if (!FORME.test(adresse)) return 'Saisissez une adresse e-mail valide.';
  return mdp ? null : 'Saisissez votre mot de passe pour confirmer.';
}

const TEXTES = {
  400: 'Cette adresse e-mail n\'est pas valide.',
  401: 'Mot de passe incorrect.',
  403: 'Un compte invité ne peut pas avoir d\'adresse e-mail.',
  409: 'Cette adresse est déjà validée par un autre compte.',
  429: 'Trop d\'envois, réessayez dans une heure.',
};

export const texteEmail = (r) => TEXTES[r.status] || r.data?.erreur || 'Opération impossible.';
