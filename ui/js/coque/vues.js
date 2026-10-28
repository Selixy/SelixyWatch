import { cadre, cadres, canalMemorise } from './cadres.js';
import { analyserHash, transmettre } from './ouverture.js';

const VUES = ['room', 'playlists', 'profil'];
const TITRES = { room: 'Room', playlists: 'Playlists', profil: 'Profil' };
let courante = null;

export function marquer() {
  for (const a of document.querySelectorAll('a[data-vue]')) {
    if (a.dataset.vue === courante) a.setAttribute('aria-current', 'page'); else a.removeAttribute('aria-current');
  }
}

export function afficher(hash) {
  const { vue: v, id } = analyserHash(hash);
  if (id && (v === 'room' || v === 'playlists')) {
    transmettre(v, id);
    history.replaceState(null, '', '#' + v);
  }
  return afficherVue(VUES.includes(v) ? v : 'room');
}

function afficherVue(v) {
  if (v === 'room' && !canalMemorise()) { v = 'playlists'; history.replaceState(null, '', '#playlists'); }
  const f = cadre(v);
  if (!f.getAttribute('src')) f.src = f.dataset.src;
  for (const x of cadres()) x.classList.toggle('actif', x === f);
  courante = v;
  document.title = `${TITRES[v]} · SelixyWatch`;
  marquer();
  f.contentWindow?.focus();
}

export const aller = (v) => { if (location.hash === '#' + v) afficher(v); else location.hash = v; };

export function brancherVues() {
  window.addEventListener('hashchange', () => afficher(location.hash.slice(1)));
  for (const f of cadres()) f.addEventListener('load', () => { if (f.classList.contains('actif')) f.contentWindow.focus(); });
}
