import { L } from './contexte.js';
import { appliquerSon, majVolume } from './volume.js';
import { majPoster } from './poster.js';
import { sonAutorise } from './autorisation.js';

export function signaler(b) {
  L.bloque = b;
  majVolume();
  majPoster();
  if (window.top !== window) parent.postMessage({ type: 'sourdine', actif: b }, location.origin);
}

export async function lire(l) {
  if (!L.mut && !sonAutorise()) { l.muet(true); signaler(true); await l.jouer().catch(() => {}); majPoster(); return; }
  l.muet(L.mut);
  try { await l.jouer(); signaler(false); }
  catch { l.muet(true); await l.jouer().catch(() => {}); signaler(!L.mut); }
  majPoster();
}

export function debloquer() {
  if (!L.bloque) return;
  appliquerSon();
  setTimeout(() => { if (!L.actif) signaler(false); else if (L.actif.estEnPause()) lire(L.actif); else signaler(false); }, 250);
}

export function initDeblocage() {
  const surGeste = () => { if (L.bloque) L.premierGeste = Date.now(); debloquer(); };
  for (const t of ['pointerdown', 'touchend', 'keydown']) document.addEventListener(t, surGeste, { capture: true, passive: true });
  setInterval(() => { if (L.bloque && navigator.userActivation?.hasBeenActive) debloquer(); }, 500);
}
