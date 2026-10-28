export function etatOffre(profil) {
  if (profil?.admin) {
    const note = profil.envoi_fichiers ? null : 'Validez votre adresse e-mail pour envoyer des fichiers.';
    return { titre: 'Administrateur · stockage illimité', note, jauge: true };
  }
  if (profil?.offre !== 'pro') {
    return { titre: 'Offre Free', note: 'Le stockage de fichiers est réservé aux comptes Pro.', jauge: false };
  }
  const note = profil.envoi_fichiers ? null : 'Validez votre adresse e-mail pour envoyer des fichiers.';
  return { titre: 'Offre Pro', note, jauge: true };
}
