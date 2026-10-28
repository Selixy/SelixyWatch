import { L, elements, courant } from './contexte.js';
import { bascule } from './actions.js';
import { repos, reveiller } from './repos.js';
import { pleinEcran } from './plein.js';

const { video, ecran } = elements;
let attente = 0, tactile = false, cachees = false;

const surImage = (e) => e.target === video || e.target === ecran || e.target.id === 'calque';

function leve() {
  if (!L.doigtPose) return;
  L.doigtPose = false;
  if (!L.masqueesParToucher) reveiller();
}

function surClic(e) {
  if (!surImage(e) || !courant()) return;
  if (tactile) {
    if (cachees || Date.now() - L.revelee < 700) { L.masqueesParToucher = false; reveiller(); }
    else { L.masqueesParToucher = true; ecran.classList.add('repos'); }
    return;
  }
  if (Date.now() - L.premierGeste < 700) return;
  if (e.detail > 1) return;
  clearTimeout(attente);
  attente = setTimeout(bascule, 250);
}

export function initPointeur() {
  ecran.addEventListener('pointerdown', (e) => {
    tactile = e.pointerType === 'touch';
    cachees = ecran.classList.contains('repos');
    L.doigtPose = true;
    reveiller();
  });
  addEventListener('pointerup', leve, true);
  addEventListener('pointercancel', leve, true);
  ecran.addEventListener('pointermove', (e) => {
    if (e.pointerType !== 'touch') { L.masqueesParToucher = false; reveiller(); }
    else if (!L.masqueesParToucher) reveiller();
  });
  ecran.addEventListener('pointerleave', (e) => { if (e.pointerType === 'mouse') { L.dernierGeste = 0; repos(); } });
  ecran.addEventListener('click', surClic);
  ecran.addEventListener('dblclick', (e) => {
    if (!surImage(e)) return;
    clearTimeout(attente);
    pleinEcran();
  });
}
