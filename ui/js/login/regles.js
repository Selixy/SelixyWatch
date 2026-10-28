export const MDP_MIN = 8;
export const MDP_MAX = 128;

const erreurMdp = (mdp) => {
  if (mdp.length < MDP_MIN) return `Le mot de passe doit contenir au moins ${MDP_MIN} caractères.`;
  return mdp.length > MDP_MAX ? `Le mot de passe ne peut pas dépasser ${MDP_MAX} caractères.` : null;
};

export function erreurSaisie(mode, { pseudo, mdp, confirmation }) {
  if (pseudo.length < 2) return 'Le pseudo doit contenir au moins 2 caractères.';
  if (mode === 'connexion') return mdp ? null : 'Saisissez votre mot de passe.';
  return erreurMdp(mdp) || (mdp === confirmation ? null : 'Les deux mots de passe ne correspondent pas.');
}

export function erreurNouveau({ nouveau, confirmation }) {
  return erreurMdp(nouveau) || (nouveau === confirmation ? null : 'Les deux mots de passe ne correspondent pas.');
}

export function erreurChangement({ ancien, nouveau, confirmation }) {
  return ancien ? erreurNouveau({ nouveau, confirmation }) : 'Saisissez votre mot de passe actuel.';
}

export const texteServeur = (r, defaut) => r.data?.erreur
  || (r.status === 429 ? 'Trop de tentatives, réessayez dans quelques minutes.' : r.data?.message || defaut);
