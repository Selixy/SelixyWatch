import { CHEMIN_FENTE_S } from './formes.js';
import { geometrieLame } from './lame-geometrie.js';
import { formesEtZones, echelleDuS } from './defs-formes.js';

const DILATE = 'fill="#000" stroke="#000" stroke-width="3.2" stroke-linejoin="round"';

const masque = (p, nom, contenu) => `<mask id="${p}-${nom}" maskUnits="userSpaceOnUse" x="0" y="0" width="64" height="64"><rect width="64" height="64" fill="#fff"/>${contenu}</mask>`;
const dilate = (p, region, formes) => `<g clip-path="url(#${p}-${region})" ${DILATE}>${formes}</g>`;
const jour = (p, region) => `<g clip-path="url(#${p}-${region})"><use href="#${p}-BHx" fill="#000"/></g>`;

function masques(p, echelleS) {
  const cadre = `<use href="#${p}-FR"/><use href="#${p}-FT"/>`;
  return masque(p, 'mB', dilate(p, 'haut', `<use href="#${p}-S"/>`) + dilate(p, 'haut', cadre)) +
    masque(p, 'd', dilate(p, 'bas_et_droite', cadre)) +
    masque(p, 'mS', jour(p, 'milieu')) +
    masque(p, 'mF', `<g clip-path="url(#${p}-fente)"><path d="${CHEMIN_FENTE_S}"${echelleDuS(echelleS)} fill="#000"/></g>` + jour(p, 'bas'));
}

export function definitions(p, etat, echelleS = 1) {
  return `<defs>${formesEtZones(p, geometrieLame(etat), echelleS)}${masques(p, echelleS)}</defs>`;
}
