import { AXE_LAME } from './formes.js';

export const REPERE = `translate(${AXE_LAME.x} ${AXE_LAME.y}) rotate(${AXE_LAME.angle})`;
export const REPERE_INVERSE = `rotate(${-AXE_LAME.angle}) translate(${-AXE_LAME.x} ${-AXE_LAME.y})`;
const BORD_DROIT = AXE_LAME.longueur + 2;
const LARGEUR_REVELEE = AXE_LAME.longueur + 4;

export function geometrieLame(etat) {
  const largeur = LARGEUR_REVELEE * etat.largeur;
  return { x: BORD_DROIT - largeur, largeur, echelle: etat.epaisseur };
}

export function appliquerLame(racine, etat) {
  const g = geometrieLame(etat);
  const fenetre = racine.querySelector('[data-rev]');
  fenetre.setAttribute('x', g.x);
  fenetre.setAttribute('width', g.largeur);
  racine.querySelectorAll('[data-echelle]').forEach((e) => e.setAttribute('transform', `scale(1 ${g.echelle})`));
}
