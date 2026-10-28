import { api } from './api.js';
import { $, esc } from './ui.js';
import { initRondSon } from './son.js';

export async function moi() {
  const r = await api('/api/moi');
  return r.ok && !r.data?.anonyme ? r.data : null;
}

export const deconnecter = () => api('/api/deconnexion', { method: 'POST' });

const contenu = (m) => m
  ? `${m.avatar ? `<img class="avatar-mini" src="${esc(m.avatar)}" alt="" width="22" height="22">` : ''}<span>${esc(m.pseudo)}</span>`
  : 'Login';

export function afficherCompte(m) {
  const compte = $('#compte');
  if (!compte) return;
  const courant = location.hash === '#profil' ? ' aria-current="page"' : '';
  compte.innerHTML = `<a class="tab tab-moi" href="#profil" data-vue="profil"${courant}>${contenu(m)}</a>`;
}

export async function initCompte() {
  initRondSon();
  const m = await moi();
  afficherCompte(m);
  return m;
}
