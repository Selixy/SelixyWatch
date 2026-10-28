import { icone } from './ui.js';
import { S, demarrer, surChangement, choisirCanal, etat, agir } from './etat.js';
import { initLecteur, rendreSon } from './lecteur.js';
import { initCompte } from './compte.js';
import { initPresence } from './presence.js';
import { initChat } from './chat.js';
import { initNotifs } from './notifs.js';
import { initAcces } from './acces.js';

const ailleurs = () => (window.top !== window ? parent.postMessage({ type: 'aller', vue: 'playlists' }, location.origin) : location.replace('/#playlists'));
if (!S.canal) ailleurs();
else {
  document.querySelectorAll('[data-icone]').forEach((el) => el.insertAdjacentHTML('afterbegin', icone(el.dataset.icone, 20)));

  surChangement(() => { if (!S.canal && !S.refuse) ailleurs(); });
  window.addEventListener('message', (e) => {
    if (e.origin !== location.origin) return;
    if (e.data?.type === 'room') {
      if (e.data.id === S.canal && e.data.entrer) {
        if (!etat()?.lecture) agir('lire').catch(() => {});
      } else {
        choisirCanal(e.data.id);
      }
    } else if (e.data?.type === 'geste') rendreSon();
  });
  initLecteur();
  initCompte();
  initPresence();
  initChat();
  initNotifs();
  initAcces();
  demarrer();
}
