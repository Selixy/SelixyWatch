import { esc } from './dom.js';

export function avatar(m, taille = 24) {
  const nom = m?.pseudo || 'Anonyme';
  if (m?.avatar) return `<img class="avatar" src="${esc(m.avatar)}" alt="" width="${taille}" height="${taille}" title="${esc(nom)}">`;
  let h = 0;
  for (const c of nom) h = (h * 31 + c.codePointAt(0)) % 360;
  return `<span class="avatar avatar--lettre" style="--t:${taille}px;--h:${h}" title="${esc(nom)}">${esc([...nom][0].toUpperCase())}</span>`;
}
