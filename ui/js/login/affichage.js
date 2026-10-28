import { $, avatar } from '../ui.js';
import { saisie } from './saisie.js';

export const message = (t, ok = false, cible = '#message') => { const m = $(cible); m.textContent = t || ''; m.classList.toggle('ok', ok); };

export function apercu() {
  const pseudo = $('#pseudo').value.trim() || saisie.profil?.pseudo || '?';
  const src = saisie.image ? URL.createObjectURL(saisie.image) : saisie.retirer ? null : saisie.profil?.avatar;
  $('#apercu').innerHTML = avatar({ pseudo, avatar: src }, 72);
  $('#retirer-avatar').hidden = !src;
}
