import { MOT } from './formes-texte.js';

const HAUTEUR_REPERE = 64;
const LIGNE_DE_BASE = 55.5;

export function construireMot({ taille = 34 } = {}) {
  const largeur = (taille * MOT.largeur) / HAUTEUR_REPERE;
  const hauteur = (taille * MOT.hauteur) / HAUTEUR_REPERE;
  const chemins = MOT.chemins.map((d) => `<path d="${d}"/>`).join('');
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="${MOT.gauche} ${MOT.haut} ${MOT.largeur} ${MOT.hauteur}" width="${largeur.toFixed(1)}" height="${hauteur.toFixed(1)}" ` +
    `aria-hidden="true" focusable="false" fill="currentColor" fill-rule="evenodd"><g transform="translate(0 ${LIGNE_DE_BASE})">${chemins}</g></svg>`;
}

export function monterMot(lien, taille) {
  if (!lien) return;
  lien.setAttribute('aria-label', 'SelixyWatch');
  lien.innerHTML = construireMot({ taille });
}
