import { $ } from '../ui.js';
import { initMarque } from '../marque/index.js';
import { initJauge } from './jauge.js';
import { estMuet, fixerMuet, estCleMuet } from './reglage.js';
import { estForcee } from './sourdine.js';

function afficher(b, marque) {
  const coupe = estMuet() || estForcee();
  b.classList.toggle('coupe', coupe);
  marque.definirCoupe(coupe);
  b.setAttribute('aria-pressed', String(coupe));
  b.setAttribute('aria-label', coupe ? 'Réactiver le son' : 'Couper le son');
  b.title = coupe ? 'Son coupé (pour moi seulement)' : 'Couper le son (pour moi seulement)';
}

function basculer() {
  if (estForcee()) { window.dispatchEvent(new Event('rond-geste')); return; }
  fixerMuet(!estMuet());
  window.dispatchEvent(new Event('son-local'));
}

export function initRondSon() {
  const b = $('#rond-son');
  if (!b) return;
  const lien = $('.marque a');
  const marque = initMarque(b, lien);
  initJauge(lien);
  const maj = () => afficher(b, marque);
  b.onclick = basculer;
  window.addEventListener('son-local', maj);
  window.addEventListener('storage', (e) => { if (estCleMuet(e.key)) maj(); });
  maj();
}
