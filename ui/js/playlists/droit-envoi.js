import { $ } from '../ui.js';
import { mentionEnvoi } from './messages-envoi.js';

export const droit = { autorise: true };

export function appliquerDroitEnvoi(profil) {
  const mention = mentionEnvoi(profil);
  droit.autorise = !mention;
  $('#vue-importer').hidden = !!mention;
  const lieu = $('#mention-envoi');
  lieu.hidden = !mention;
  if (!mention) return;
  lieu.textContent = mention.texte;
  if (mention.lien) lieu.setAttribute('href', mention.lien); else lieu.removeAttribute('href');
}
