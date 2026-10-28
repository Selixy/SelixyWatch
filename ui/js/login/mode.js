import { $ } from '../ui.js';
import { message } from './affichage.js';

export const mode = { courant: 'connexion' };

export function choisirMode(m) {
  mode.courant = m;
  const inscription = m === 'inscription';
  $('#confirmation-champ').hidden = !inscription;
  $('#mdp').autocomplete = inscription ? 'new-password' : 'current-password';
  $('#lien-oubli').hidden = inscription;
  $('#valider-auth').textContent = inscription ? 'Créer le compte' : 'Se connecter';
  for (const b of document.querySelectorAll('[data-mode]')) b.setAttribute('aria-pressed', String(b.dataset.mode === m));
  message('', false, '#message-auth');
}

export function brancherModes() {
  for (const b of document.querySelectorAll('[data-mode]')) b.onclick = () => choisirMode(b.dataset.mode);
  choisirMode('connexion');
}
