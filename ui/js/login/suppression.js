import { api } from '../api.js';
import { $ } from '../ui.js';
import { message } from './affichage.js';
import { texteServeur } from './regles.js';
import { retourner, prevenirCoque } from './redirection.js';

const CIBLE = '#message-suppression';

async function supprimer(e) {
  e.preventDefault();
  const mdp = $('#mdp-suppression').value;
  if (!mdp) return message('Saisissez votre mot de passe pour confirmer.', false, CIBLE);
  const r = await api('/api/moi/supprimer', { method: 'POST', body: { mdp } });
  if (!r.ok) return message(texteServeur(r, 'Suppression impossible.'), false, CIBLE);
  prevenirCoque();
  retourner();
}

const basculer = (ouvert) => {
  $('#form-suppression').hidden = !ouvert;
  $('#demander-suppression').hidden = ouvert;
  if (ouvert) $('#mdp-suppression').focus();
};

export function brancherSuppression() {
  $('#demander-suppression').onclick = () => basculer(true);
  $('#annuler-suppression').onclick = () => { $('#form-suppression').reset(); message('', false, CIBLE); basculer(false); };
  $('#form-suppression').onsubmit = supprimer;
}
