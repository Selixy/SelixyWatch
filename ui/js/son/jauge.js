import { estMuet, estCleMuet } from './reglage.js';
import { volumeMaitre, fixerVolumeMaitre, estCleVolume } from './volume-maitre.js';

function creerJauge() {
  const entree = Object.assign(document.createElement('input'), { type: 'range', min: 0, max: 1, step: 0.01, className: 'jauge-son' });
  entree.setAttribute('aria-label', 'Volume général');
  return entree;
}

function afficher(entree) {
  const niveau = estMuet() ? 0 : volumeMaitre();
  entree.value = niveau;
  entree.style.setProperty('--rempli', `${Math.round(niveau * 100)}%`);
  entree.setAttribute('aria-valuetext', `${Math.round(niveau * 100)} %`);
}

export function initJauge(lien) {
  if (!lien) return;
  const mot = Object.assign(document.createElement('div'), { className: 'mot' });
  const entree = creerJauge();
  lien.replaceWith(mot);
  mot.append(lien, entree);
  const maj = () => afficher(entree);
  entree.addEventListener('input', () => {
    fixerVolumeMaitre(+entree.value);
    window.dispatchEvent(new Event('son-local'));
  });
  mot.addEventListener('pointerleave', () => { if (document.activeElement === entree && !entree.matches(':focus-visible')) entree.blur(); });
  window.addEventListener('son-local', maj);
  window.addEventListener('storage', (e) => { if (estCleMuet(e.key) || estCleVolume(e.key)) maj(); });
  maj();
}
