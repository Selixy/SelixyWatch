import { $ } from '../ui.js';
import { elements } from './contexte.js';
import { lireLocal, ecrireLocal } from './stockage.js';

export function cinema(actif = !elements.salle.classList.contains('cinema')) {
  elements.salle.classList.toggle('cinema', actif);
  $('#cinema').setAttribute('aria-pressed', String(actif));
  ecrireLocal('mu-cinema', actif ? '1' : '0');
}

export function initCinema() {
  cinema(lireLocal('mu-cinema', '0') === '1');
  $('#cinema').onclick = () => cinema();
}
