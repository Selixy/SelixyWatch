import { initCompte } from '../compte.js';
import { sourdineForcee } from '../son.js';
import { cadre } from './cadres.js';
import { aller, marquer } from './vues.js';

const COMMANDES = {
  aller: (d) => aller(d.vue),
  compte: () => initCompte().then(marquer),
  sourdine: (d) => sourdineForcee(!!d.actif),
  plein: (d) => document.documentElement.classList.toggle('plein', !!d.actif),
  recharger: (d) => { history.replaceState(null, '', '#' + (d.vue || 'room')); location.reload(); },
  entrer: (d) => {
    const room = cadre('room'), chargee = !!room.getAttribute('src');
    aller('room');
    if (chargee) {
      room.contentWindow.postMessage({ type: 'room', id: d.id, entrer: true }, location.origin);
      room.contentWindow.postMessage({ type: 'geste' }, location.origin);
    }
  },
};

export function brancherMessages() {
  window.addEventListener('message', (e) => {
    if (e.origin !== location.origin) return;
    const d = e.data || {};
    if (Object.hasOwn(COMMANDES, d.type)) COMMANDES[d.type](d);
  });
  window.addEventListener('rond-geste', () => cadre('room').contentWindow?.postMessage({ type: 'geste' }, location.origin));
}
