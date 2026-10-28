import { construireMarque } from './logo.js';
import { appliquerLame } from './lame-geometrie.js';
import { jouerSequence } from './chronologie.js';
import { SEQUENCES, etatLame, ETAT_ABSENTE, ETAT_PRESENTE } from './lame-rythme.js';

const mouvementReduit = () => matchMedia('(prefers-reduced-motion: reduce)').matches;

export function monterEntete(bouton, taille = 34, options = {}) {
  bouton.innerHTML = construireMarque({ taille, ...options });
  const svg = bouton.querySelector('svg');
  let arreter = () => {};
  return (coupe, animer) => {
    arreter();
    const final = coupe ? ETAT_PRESENTE : ETAT_ABSENTE;
    const sequence = SEQUENCES[coupe ? 'apparition' : 'disparition'];
    if (!animer || mouvementReduit()) { appliquerLame(svg, final); return; }
    arreter = jouerSequence(sequence, (t) => appliquerLame(svg, etatLame(sequence, t)), () => appliquerLame(svg, final));
  };
}
