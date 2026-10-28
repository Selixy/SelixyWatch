import { $, esc, avatar } from './ui.js';

const lire = (k, d) => { try { return localStorage.getItem(k) ?? d; } catch { return d; } };
let actif = lire('mu-notifs', '1') !== '0';

export function initNotifs() {
  const b = $('#notifs-bascule');
  const maj = () => {
    b.setAttribute('aria-pressed', String(actif));
    b.title = actif ? 'Messages du chat sur la vidéo : activés' : 'Messages du chat sur la vidéo : désactivés';
  };
  b.onclick = () => {
    actif = !actif;
    try { localStorage.setItem('mu-notifs', actif ? '1' : '0'); } catch {}
    if (!actif) $('#notifs').replaceChildren();
    maj();
  };
  maj();
}

function chatReplie() {
  const salle = $('#salle');
  if (salle.classList.contains('plein')) return !salle.classList.contains('chat-ouvert');
  return matchMedia('(max-width: 899px)').matches && salle.dataset.devant !== 'chat';
}

export function annoncer(m) {
  if (!actif || !chatReplie()) return;
  const zone = $('#notifs');
  const el = document.createElement('div');
  el.className = 'notif';
  el.innerHTML = `${avatar(m.auteur, 26)}<div><b>${esc(m.auteur.pseudo)}</b>${esc(m.texte)}</div>`;
  zone.append(el);
  while (zone.children.length > 3) zone.firstElementChild.remove();
  setTimeout(() => { el.classList.add('part'); setTimeout(() => el.remove(), 480); }, 4800);
}
