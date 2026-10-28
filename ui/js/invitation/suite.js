import { api } from '../api.js';
import { accepter } from './acceptation.js';
import { enAttente, effacer } from './jeton.js';
import { entrerDans } from './destination.js';

export const contexteNavigateur = () => ({
  stockage: localStorage,
  cadre: window.top !== window,
  parent: window.parent,
  aller: (url) => { location.href = url; },
});

export async function accepterEtEntrer(jeton) {
  const r = await accepter(api, jeton);
  if (r.erreur) return r;
  effacer(sessionStorage);
  if (r.noeuds.length) entrerDans(r.noeuds,contexteNavigateur());
  return r;
}

export const suiteEnAttente = () => {
  const jeton = enAttente(sessionStorage);
  return jeton ? accepterEtEntrer(jeton) : null;
};
