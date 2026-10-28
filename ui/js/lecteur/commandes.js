import { $ } from '../ui.js';
import { agir } from '../etat.js';
import { bascule } from './actions.js';
import { erreur } from './messages.js';
import { pleinEcran } from './plein.js';

export function initCommandes() {
  $('#lire').onclick = bascule;
  $('#grand-lire').onclick = bascule;
  for (const b of document.querySelectorAll('.act-prec')) b.onclick = () => agir('precedent').catch(erreur);
  for (const b of document.querySelectorAll('.act-suiv')) b.onclick = () => agir('suivant').catch(erreur);
  $('#plein').onclick = pleinEcran;
}
