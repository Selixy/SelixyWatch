import { api } from '../api.js';
import { $ } from '../ui.js';
import { message } from './affichage.js';
import { creerAnonyme } from '../invitation/anonyme.js';
import { terminerConnexion } from './suite-connexion.js';

async function entrer() {
  const bouton = $('#entrer-anonyme');
  bouton.disabled = true;
  try {
    const r = await creerAnonyme(api);
    if (r.erreur) return message(r.erreur, false, '#message-auth');
    await terminerConnexion(r.profil);
  } finally {
    bouton.disabled = false;
  }
}

export const brancherAnonyme = () => { $('#entrer-anonyme').onclick = entrer; };
