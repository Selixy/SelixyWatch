import { api } from '../api.js';
import { $ } from '../ui.js';
import { message } from './affichage.js';
import { erreurChangement, texteServeur } from './regles.js';

const CIBLE = '#message-mdp';

async function changer(e) {
  e.preventDefault();
  const s = { ancien: $('#mdp-ancien').value, nouveau: $('#mdp-nouveau').value, confirmation: $('#mdp-confirmation').value };
  const erreur = erreurChangement(s);
  if (erreur) return message(erreur, false, CIBLE);
  const r = await api('/api/moi/mdp', { method: 'POST', body: { ancien: s.ancien, nouveau: s.nouveau } });
  if (!r.ok) return message(texteServeur(r, 'Changement impossible.'), false, CIBLE);
  e.target.reset();
  message('Mot de passe modifié. Les autres appareils sont déconnectés.', true, CIBLE);
}

export const brancherMdp = () => { $('#form-mdp').onsubmit = changer; };
