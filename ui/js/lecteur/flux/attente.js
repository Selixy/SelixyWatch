export const attendre = (tampon, action) => new Promise((resolu, rejete) => {
  const fin = () => { tampon.removeEventListener('error', erreur); resolu(); };
  const erreur = (cause) => { tampon.removeEventListener('updateend', fin); rejete(cause instanceof Error ? cause : new Error('tampon en erreur')); };
  tampon.addEventListener('updateend', fin, { once: true });
  tampon.addEventListener('error', erreur, { once: true });
  try { action(); } catch (cause) { erreur(cause); }
});
