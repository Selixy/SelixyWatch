import { $, duree } from '../ui.js';
import { cible } from '../etat.js';
import { L, courant, longueur } from './contexte.js';
import { aller } from './actions.js';

export function tic() {
  const d = longueur();
  const pos = L.glisse !== null ? L.glisse * d : Math.min(cible(), d || Infinity);
  const ok = courant() && d;
  const texte = courant() ? `${duree(pos)} / ${d ? '−' + duree(Math.max(0, d - pos)) : '–:––'}` : '';
  $('#temps').textContent = $('#temps-lu').textContent = texte;
  $('#barre-i').style.width = ok ? `${(pos / d) * 100}%` : '0';
  $('#barre').setAttribute('aria-valuenow', ok ? String(Math.round((pos / d) * 100)) : '0');
}

function fractionDe(ev) {
  const r = $('#barre').getBoundingClientRect();
  return Math.max(0, Math.min(1, (ev.clientX - r.left) / r.width));
}

export function initBarre() {
  const barre = $('#barre');
  barre.addEventListener('pointerdown', (e) => {
    if (!courant()) return;
    e.preventDefault();
    barre.setPointerCapture(e.pointerId);
    L.glisse = fractionDe(e);
    barre.classList.add('glisse');
    tic();
  });
  barre.addEventListener('pointermove', (e) => { if (L.glisse !== null) { L.glisse = fractionDe(e); tic(); } });
  const relache = (e) => {
    if (L.glisse === null) return;
    const f = e.type === 'pointerup' ? fractionDe(e) : null;
    L.glisse = null;
    barre.classList.remove('glisse');
    if (f !== null) aller(f * longueur());
    tic();
  };
  barre.addEventListener('pointerup', relache);
  barre.addEventListener('pointercancel', relache);
  setInterval(tic, 250);
}
