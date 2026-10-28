import { conteneur, zoneVue } from './elements.js';

export function effacerIndicateurs() {
  document.querySelectorAll('.drop-avant, .drop-apres, .drop-dans').forEach((x) => x.classList.remove('drop-avant', 'drop-apres', 'drop-dans'));
  conteneur.classList.remove('drop-fond');
  zoneVue.classList.remove('drop-fond');
}

export function indiquer(d) {
  effacerIndicateurs();
  if (d.zone === 'fond') conteneur.classList.add('drop-fond');
  else d.ligne.classList.add(`drop-${d.zone}`);
}
