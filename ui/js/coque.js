import { initCompte } from './compte.js';
import { afficher, marquer, brancherVues } from './coque/vues.js';
import { brancherMessages } from './coque/messages.js';
import { brancherZones, mesurerZones } from './coque/zones.js';
import { suivreClavier } from './coque/clavier.js';

brancherVues();
brancherMessages();
brancherZones();
suivreClavier();
mesurerZones();

const entete = document.querySelector('.header');
entete?.addEventListener('wheel', (e) => {
  if (e.target.closest?.('.mot, .jauge-son, .rond-son')) return;
  const f = document.querySelector('iframe.actif');
  f?.contentWindow?.scrollBy({ top: e.deltaY, left: e.deltaX });
}, { passive: true });

window.addEventListener('keydown', (e) => {
  if (e.ctrlKey || e.altKey || e.metaKey) return;
  if (e.target.closest?.('input, textarea, select, [contenteditable]')) return;
  if (e.key === ' ' || e.code === 'Space') {
    const f = document.querySelector('iframe.actif');
    if (f?.dataset.vue === 'room') {
      e.preventDefault();
      f.contentDocument?.dispatchEvent(new KeyboardEvent('keydown', {
        key: ' ', code: 'Space', bubbles: true, cancelable: true
      }));
    }
  }
});

afficher(location.hash.slice(1));
initCompte().then(marquer);
