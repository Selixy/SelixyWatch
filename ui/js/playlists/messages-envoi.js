export function mentionEnvoi(profil) {
  if (!profil || profil.envoi_fichiers) return null;
  if (profil.offre === 'pro') return { texte: 'Validez votre e-mail', lien: '/#profil' };
  return { texte: 'Envoi de fichiers : offre Pro', lien: null };
}

const TEXTES = {
  402: 'L\'envoi de fichiers est réservé aux comptes Pro.',
  403: 'Validez votre adresse e-mail pour envoyer des fichiers.',
  413: 'Fichier trop gros.',
  507: 'Votre espace de stockage est plein.',
};

export const texteEchecEnvoi = (statut, donnees) => TEXTES[statut] || donnees?.erreur || 'Envoi impossible.';
