import { definitions } from './defs.js';
import { ETAT_ABSENTE } from './lame-rythme.js';

export function construireMarque({ encre = 'currentColor', prefixe = 'mq', etat = ETAT_ABSENTE, taille = 64, echelleS = 1, opaciteTele = 1, couleurLame = encre } = {}) {
  const p = prefixe;
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="${taille}" height="${taille}" aria-hidden="true" focusable="false">${definitions(p, etat, echelleS)}` +
    `<g fill="${encre}"><g mask="url(#${p}-mB)"><use href="#${p}-BLx" fill="${couleurLame}"/></g><g mask="url(#${p}-mS)"><use href="#${p}-S" mask="url(#${p}-d)"/></g>` +
    `<g opacity="${opaciteTele}"><g mask="url(#${p}-mF)"><use href="#${p}-FR"/></g><use href="#${p}-FT"/></g><g clip-path="url(#${p}-sous)"><use href="#${p}-BLx" fill="${couleurLame}"/></g></g></svg>`;
}
