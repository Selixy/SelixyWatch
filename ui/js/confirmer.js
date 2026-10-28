import { api } from './api.js';
import { $ } from './ui.js';
import { lireJeton } from './invitation/jeton.js';
import { confirmer } from './confirmer/appel.js';

const dire = (texte, erreur = false) => {
  const m = $('#message');
  m.textContent = texte;
  m.classList.toggle('erreur', erreur);
};

async function lancer() {
  const jeton = lireJeton(location.hash);
  history.replaceState(null, '', location.pathname);
  $('#profil-lien').hidden = false;
  if (!jeton) return dire('Ce lien de confirmation est incomplet.', true);
  const r = await confirmer(api, jeton);
  if (r.erreur) return dire(r.erreur, true);
  dire(r.email ? `L'adresse ${r.email} est validée.` : 'Votre adresse est validée.');
}

lancer();
