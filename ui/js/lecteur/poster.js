import { $ } from '../ui.js';
import { etat } from '../etat.js';
import { L, elements, courant } from './contexte.js';
import { yt } from './fabrique.js';

export function majPoster() {
  const m = courant(), e = etat();
  const arret = L.actif === yt && m?.source === 'youtube' && (!e?.lecture || (L.bloque && L.actif?.estEnPause()));
  const img = $('#poster');
  elements.ecran.classList.toggle('arret', arret);
  if (!arret) return;
  const src = `https://i.ytimg.com/vi/${m.yt}/maxresdefault.jpg`;
  if (img.dataset.yt !== m.yt) {
    img.dataset.yt = m.yt;
    img.onerror = () => { img.onerror = null; img.src = `https://i.ytimg.com/vi/${m.yt}/mqdefault.jpg`; };
    img.src = src;
  }
}
