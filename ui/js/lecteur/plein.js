import { $ } from '../ui.js';
import { elements } from './contexte.js';
import { plein, etatSalle } from './salle-etat.js';
import { reveiller } from './repos.js';

const { salle } = elements;

export function majPlein(actif) {
  salle.classList.toggle('plein', actif);
  salle.classList.toggle('reel', actif && !!document.fullscreenElement);
  if (!actif) { salle.classList.remove('chat-ouvert'); $('#chat-plein').setAttribute('aria-pressed', 'false'); }
  $('#plein').setAttribute('aria-pressed', String(actif));
  etatSalle();
  reveiller();
  if (window.top !== window) parent.postMessage({ type: 'plein', actif }, location.origin);
}

export function pleinEcran() {
  if (plein()) { if (document.fullscreenElement) document.exitFullscreen().catch(() => {}); else majPlein(false); return; }
  majPlein(true);
  if (salle.requestFullscreen) salle.requestFullscreen().then(() => salle.classList.add('reel'), () => {});
}

export function initPlein() {
  document.addEventListener('fullscreenchange', () => {
    if (document.fullscreenElement) salle.classList.add('reel');
    else { salle.classList.remove('reel'); if (plein()) majPlein(false); }
  });
}
