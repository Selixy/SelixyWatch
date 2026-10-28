import { S } from './partage.js';
import { notifier } from './observateur.js';
import { ecrire } from './stockage.js';
import { connecter } from './flux.js';

export function choisirCanal(id) {
  if (id === S.canal) return;
  S.canal = id;
  S.refuse = false;
  if (id) ecrire('mu-canal', id);
  connecter();
  notifier('canal');
}

export function entrer(id) {
  if (id) ecrire('mu-canal', id);
  if (window.top !== window) parent.postMessage({ type: 'entrer', id }, location.origin);
  else {
    choisirCanal(id);
    location.href = '/#room';
  }
}
