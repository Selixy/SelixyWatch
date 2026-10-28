import { $ } from '../ui.js';
import { etatOffre } from './offre-etat.js';
import { afficherQuota } from './quota.js';

export function afficherOffre(profil) {
  const etat = etatOffre(profil);
  $('#offre-titre').textContent = etat.titre;
  $('#offre-note').textContent = etat.note || '';
  $('#offre-note').hidden = !etat.note;
  $('#quota').hidden = true;
  if (etat.jauge) afficherQuota(profil, document);
}
