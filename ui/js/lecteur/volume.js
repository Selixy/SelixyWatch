import { $, icone } from '../ui.js';
import { L } from './contexte.js';
import { lecteurs } from './fabrique.js';
import { sur } from './evenements.js';

export function appliquerSon() {
  for (const l of lecteurs) { l.volume(L.vol); l.muet(L.mut); }
}

export function majVolume() {
  const muet = L.mut || L.vol === 0 || L.bloque;
  $('#son').innerHTML = icone(muet ? 'muet' : 'volume', 22);
  $('#son').setAttribute('aria-label', muet ? 'Réactiver le son' : 'Couper le son');
  $('#volume').value = L.mut ? 0 : L.vol;
}

sur('son-a-appliquer', appliquerSon);
