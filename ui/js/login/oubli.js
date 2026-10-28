import { api } from '../api.js';
import { $ } from '../ui.js';
import { message } from './affichage.js';

const CIBLE = '#message-oubli';
export const MESSAGE_NEUTRE = 'Si un compte avec une adresse validée correspond, un lien vient de partir.';

async function envoyer(e) {
  e.preventDefault();
  const identifiant = $('#oubli-identifiant').value.trim();
  if (!identifiant) return message('Saisissez votre pseudo ou votre adresse e-mail.', false, CIBLE);
  const r = await api('/api/recuperation', { method: 'POST', body: { identifiant } });
  message(r.status === 429 ? 'Trop de demandes, réessayez dans quelques minutes.' : MESSAGE_NEUTRE, r.ok, CIBLE);
}

function montrer(oubli) {
  $('#auth').hidden = oubli;
  $('#oubli').hidden = !oubli;
  message('', false, CIBLE);
}

export function brancherOubli() {
  $('#lien-oubli').onclick = () => montrer(true);
  $('#oubli-retour').onclick = () => montrer(false);
  $('#oubli').onsubmit = envoyer;
}
