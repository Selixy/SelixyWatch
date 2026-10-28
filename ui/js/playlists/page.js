import { $ } from '../ui.js';
import { lire } from './stockage.js';

export const P = {
  selection: 'racine',
  vue: lire('mu-playlist-vue', '') || null,
  glisse: null,
  piste: null,
  edition: null,
  aRenommer: null,
  enAttente: false,
  aOuvrir: null,
  ouvrirAvant: 0,
};

export const message = (texte) => { $('#message').textContent = texte || ''; };

export async function essayer(f) {
  try { const r = await f(); message(''); return r; } catch (e) { message(e.message); return null; }
}

let rendu = () => {};
export const definirRendu = (f) => { rendu = f; };
export const rendre = () => rendu();
