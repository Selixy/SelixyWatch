import { elements } from './contexte.js';

export const plein = () => elements.salle.classList.contains('plein');
export const etatSalle = () => elements.salle.dispatchEvent(new Event('etat'));
