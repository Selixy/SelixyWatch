import { $ } from '../ui.js';
import { elements } from './contexte.js';
import { etatSalle } from './salle-etat.js';

export function chatPlein(ouvert = !elements.salle.classList.contains('chat-ouvert')) {
  elements.salle.classList.toggle('chat-ouvert', ouvert);
  $('#chat-plein').setAttribute('aria-pressed', String(ouvert));
  $('#chat-plein').setAttribute('aria-label', ouvert ? 'Replier le chat' : 'Afficher le chat');
  etatSalle();
}

export function initChatPlein() {
  $('#chat-plein').onclick = () => chatPlein();
  $('#fermer-chat').onclick = () => chatPlein(false);
}
