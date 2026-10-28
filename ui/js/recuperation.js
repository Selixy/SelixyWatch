import { api } from './api.js';
import { $ } from './ui.js';
import { lireJeton } from './invitation/jeton.js';
import { erreurNouveau } from './login/regles.js';
import { renouveler } from './recuperation/appel.js';

const dire = (texte, erreur = false) => {
  const m = $('#message');
  m.textContent = texte;
  m.classList.toggle('erreur', erreur);
};

async function envoyer(jeton) {
  const s = { nouveau: $('#mdp-nouveau').value, confirmation: $('#mdp-confirmation').value };
  const erreur = erreurNouveau(s);
  if (erreur) return dire(erreur, true);
  const r = await renouveler(api, jeton, s.nouveau);
  if (r.erreur) return dire(r.erreur, true);
  $('#form-recuperation').hidden = true;
  $('#entrer').hidden = false;
  dire('Mot de passe modifié, vous êtes connecté. Les autres appareils sont déconnectés.');
}

function lancer() {
  const jeton = lireJeton(location.hash);
  history.replaceState(null, '', location.pathname);
  if (!jeton) return dire('Ce lien de récupération est incomplet.', true);
  $('#form-recuperation').hidden = false;
  $('#form-recuperation').onsubmit = (e) => { e.preventDefault(); envoyer(jeton); };
}

lancer();
