import { $ } from '../ui.js';
import { L } from './contexte.js';
import { appliquerSon, majVolume } from './volume.js';
import { lireLocal, ecrireLocal } from './stockage.js';

export function volume(v) {
  L.mut = false;
  L.vol = Math.max(0, Math.min(1, v));
  ecrireLocal('mu-volume', L.vol);
  ecrireLocal('mu-muet', '0');
  appliquerSon();
  majVolume();
  window.dispatchEvent(new Event('son-local'));
}

export function muet() {
  if (Date.now() - L.premierGeste < 700) return;
  L.mut = !L.mut;
  ecrireLocal('mu-muet', L.mut ? '1' : '0');
  appliquerSon();
  majVolume();
  window.dispatchEvent(new Event('son-local'));
}

export function initSon() {
  L.vol = Math.max(0, Math.min(1, Number(lireLocal('mu-volume', 0.8))));
  L.mut = lireLocal('mu-muet', '0') === '1';
  const surSon = () => {
    L.mut = lireLocal('mu-muet', '0') === '1';
    L.vol = Math.max(0, Math.min(1, Number(lireLocal('mu-volume', 0.8))));
    appliquerSon();
    majVolume();
  };
  window.addEventListener('son-local', surSon);
  window.addEventListener('storage', (e) => { if (e.key === 'mu-muet' || e.key === 'mu-volume') surSon(); });
  appliquerSon();
  majVolume();
  $('#volume').oninput = (e) => volume(+e.target.value);
  $('#son').onclick = muet;
}
