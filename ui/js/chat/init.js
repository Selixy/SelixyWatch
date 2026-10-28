import { $ } from '../ui.js';
import { S, surEvenement, action } from '../etat.js';
import { moi } from '../compte.js';
import { annoncer } from '../notifs.js';
import { toutAfficher, ajouter, estMoi } from './affichage.js';

let me = null;
let messages = [];

function recevoir(d) {
  if (d.canal !== S.canal) return;
  if (d.messages) {
    messages = d.messages;
    toutAfficher(messages, me);
    return;
  }
  messages = [...messages, d.message].slice(-100);
  ajouter(d.message, me);
  if (!estMoi(d.message, me)) annoncer(d.message);
}

async function envoyer(e, champ) {
  e.preventDefault();
  const texte = champ.value.trim();
  if (!texte) return;
  champ.value = '';
  try { await action(S.canal, 'message', { texte }); }
  catch (err) { champ.value = texte; $('#message').textContent = err.message; }
}

export async function initChat() {
  surEvenement('chat', recevoir);

  me = await moi();
  $('#chat-envoi').hidden = !me;
  $('#chat-login').hidden = !!me;
  if (messages.length) toutAfficher(messages, me);

  const champ = $('#chat-texte');
  $('#chat-envoi').onsubmit = (e) => envoyer(e, champ);
}
