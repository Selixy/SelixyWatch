import { $, esc, avatar } from '../ui.js';
import { S } from '../etat.js';
import { synchroniserVocalTous, ajusterTaillesPresents } from '../vocal.js';

let premier = true;

function synchroniser(zone, items, fabrique) {
  const present = new Map([...zone.children].filter((e) => !e.classList.contains('sort')).map((e) => [e.dataset.id, e]));
  const ids = new Set(items.map((m) => m.id));
  for (const [id, el] of present) if (!ids.has(id)) { el.classList.add('sort'); setTimeout(() => el.remove(), 300); }
  for (const m of items) if (!present.has(m.id)) zone.insertAdjacentHTML('beforeend', fabrique(m));
}

export function rendre(moi) {
  const l = (S.presence?.canaux?.[S.canal] || []).map((m) => ({ ...m, moi: !!moi && m.id === moi.id }));
  const zone = $('#presents');
  zone.hidden = !S.canal || !l.length;
  zone.classList.toggle('sans-animation', premier);
  const taille = Math.max(30, Math.min(48, Math.round(50 - Math.sqrt(l.length) * 4.5)));
  zone.style.setProperty('--p-taille', `${taille}px`);
  synchroniser(zone, l, (m) =>
    `<li class="present${m.moi ? ' moi' : ''}" data-id="${esc(m.id)}" title="${esc(m.pseudo)}${m.moi ? ' (vous)' : ''}">${avatar(m, taille)}</li>`);
  premier = false;
  synchroniserVocalTous();
  ajusterTaillesPresents();
}
