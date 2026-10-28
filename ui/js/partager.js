import { actionPartage } from './partager/requetes.js';

export { ouvrirPartage } from './partager/panneau.js';
export { ouvrirInviter } from './partager/inviter.js';
export const quitter = (id) => actionPartage(id, 'quitter');
