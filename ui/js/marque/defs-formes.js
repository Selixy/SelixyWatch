import { CHEMIN_S, CHEMIN_CADRE, CHEMIN_PIED, CHEMIN_LAME, CHEMIN_JOUR_LAME } from './formes.js';
import { REPERE, REPERE_INVERSE } from './lame-geometrie.js';

export const REGIONS = { haut: 'M0 0H64V30H0Z', milieu: 'M0 30H64V47H0Z', bas: 'M0 47H64V64H0Z', sous: 'M0 30H64V64H0Z', bas_et_droite: 'M0 32H64V64H0ZM40 0H64V32H40Z', fente: 'M0 0H40V32H0Z' };

function lameAnimee(p, nom, echelle) {
  return `<g id="${p}-${nom}x" clip-path="url(#${p}-rev)"><g transform="${REPERE}"><g data-echelle="" transform="scale(1 ${echelle})"><g transform="${REPERE_INVERSE}"><use href="#${p}-${nom}"/></g></g></g></g>`;
}

export function echelleDuS(k) {
  return k === 1 ? '' : ` transform="translate(33 50) scale(${k}) translate(-33 -50)"`;
}

function zones(p) {
  return Object.entries(REGIONS).map(([nom, d]) => `<clipPath id="${p}-${nom}"><path d="${d}"/></clipPath>`).join('');
}

export function formesEtZones(p, g, echelleS = 1) {
  return `<path id="${p}-S" d="${CHEMIN_S}"${echelleDuS(echelleS)}/><path id="${p}-FR" fill-rule="evenodd" d="${CHEMIN_CADRE}"/><path id="${p}-FT" d="${CHEMIN_PIED}"/>` +
    `<path id="${p}-BL" d="${CHEMIN_LAME}"/><path id="${p}-BH" d="${CHEMIN_JOUR_LAME}"/>` +
    `<clipPath id="${p}-rev"><rect data-rev="" transform="${REPERE}" y="-16" height="32" x="${g.x}" width="${g.largeur}"/></clipPath>` +
    lameAnimee(p, 'BL', g.echelle) + lameAnimee(p, 'BH', g.echelle) + zones(p);
}
