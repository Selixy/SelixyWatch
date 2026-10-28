import { api } from './api.js';
import { $ } from './ui.js';
import { moi } from './compte.js';
import { lireJeton, garder } from './invitation/jeton.js';
import { voir } from './invitation/acceptation.js';
import { phrase } from './invitation/phrase.js';
import { creerAnonyme } from './invitation/anonyme.js';
import { accepterEtEntrer } from './invitation/suite.js';

const dire = (texte, erreur = false) => {
  const m = $('#message');
  m.textContent = texte;
  m.classList.toggle('erreur', erreur);
};

async function continuerAnonyme(jeton) {
  const c = await creerAnonyme(api);
  if (c.erreur) return dire(c.erreur, true);
  const r = await accepterEtEntrer(jeton);
  if (r.erreur) dire(r.erreur, true);
}

async function lancer() {
  const jeton = lireJeton(location.hash);
  if (!jeton) return dire('Ce lien d\'invitation est incomplet.', true);
  const vue = await voir(api, jeton);
  if (vue.erreur) return dire(vue.erreur, true);
  dire(phrase(vue.invitation));
  if (!(await moi())) {
    garder(sessionStorage, jeton);
    $('#connexion').hidden = false;
    $('#anonyme').hidden = false;
    $('#anonyme').onclick = () => continuerAnonyme(jeton);
    return;
  }
  const r = await accepterEtEntrer(jeton);
  if (r.erreur) dire(r.erreur, true);
}

lancer();
