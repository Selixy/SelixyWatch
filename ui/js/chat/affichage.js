import { $, esc, avatar } from '../ui.js';

const liste = $('#messages');

const heure = (t) => new Date(t * 1000).toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' });

export const estMoi = (m, moi) => !!moi && m.auteur.id === moi.id;

const ligne = (m, moi) =>
  `<li class="msg${estMoi(m, moi) ? ' moi' : ''}" data-id="${esc(m.id)}">${avatar(m.auteur, 28)}` +
  `<div class="msg-corps"><div class="msg-tete"><span class="msg-pseudo">${esc(m.auteur.pseudo)}</span><span class="msg-heure">${heure(m.t)}</span></div>` +
  `<p class="msg-texte">${esc(m.texte)}</p></div></li>`;

export function toutAfficher(messages, moi) {
  liste.innerHTML = messages.map((m) => ligne(m, moi)).join('');
  liste.scrollTop = liste.scrollHeight;
}

export function ajouter(message, moi) {
  const colle = liste.scrollHeight - liste.scrollTop - liste.clientHeight < 80 || estMoi(message, moi);
  liste.insertAdjacentHTML('beforeend', ligne(message, moi));
  while (liste.children.length > 100) liste.firstElementChild.remove();
  if (colle) liste.scrollTop = liste.scrollHeight;
}
