import { message } from './affichage.js';
import { retourner, prevenirCoque } from './redirection.js';
import { suiteEnAttente } from '../invitation/suite.js';

const ATTENTE_MESSAGE_MS = 1400;
const pause = (ms) => new Promise((ok) => setTimeout(ok, ms));

export async function terminerConnexion(profil) {
  if (profil?.active) {
    message('Mot de passe enregistré.', true, '#message-auth');
    await pause(ATTENTE_MESSAGE_MS);
  }
  prevenirCoque();
  const suite = suiteEnAttente();
  if (!suite) return retourner();
  const r = await suite;
  if (r.erreur) {
    message(r.erreur, false, '#message-auth');
    await pause(ATTENTE_MESSAGE_MS * 2);
    retourner();
  }
}
