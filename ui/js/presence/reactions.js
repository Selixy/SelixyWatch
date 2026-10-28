import { $, esc, avatar } from '../ui.js';
import { S, surEvenement, action } from '../etat.js';

const EMOJIS = ['❤️', '😂', '😮', '👏', '🔥', '🎉'];

function lancer(emoji, auteur) {
  const r = document.createElement('div');
  r.className = 'reac';
  r.style.left = `${55 + Math.random() * 36}%`;
  r.innerHTML = `<span class="reac-e">${esc(emoji)}</span>${avatar(auteur, 22)}`;
  $('#flotte').append(r);
  setTimeout(() => r.remove(), 3700);
}

export function initReactions() {
  const menu = $('#menu-emoji'), bouton = $('#reagir');
  bouton.hidden = true;
  menu.innerHTML = EMOJIS.map((e) => `<button type="button" role="menuitem" data-e="${e}" aria-label="Réagir ${e}">${e}</button>`).join('');
  const ouvrir = (b) => { menu.hidden = !b; bouton.setAttribute('aria-expanded', String(b)); };
  bouton.addEventListener('click', (e) => { e.stopPropagation(); ouvrir(menu.hidden); });
  menu.addEventListener('click', (e) => {
    const b = e.target.closest('[data-e]');
    if (b) action(S.canal, 'reaction', { emoji: b.dataset.e }).catch(() => {});
  });
  document.addEventListener('click', (e) => { if (!menu.hidden && !e.target.closest('.reagir')) ouvrir(false); });
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && !menu.hidden) { ouvrir(false); bouton.focus(); } });
  surEvenement('reaction', (d) => { if (d.canal === S.canal) lancer(d.emoji, d.auteur); });
}
