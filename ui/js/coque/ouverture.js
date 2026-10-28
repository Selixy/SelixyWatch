import { cadre } from './cadres.js';

const FORME_ID = /^[0-9a-f]{12}$/;

export function analyserHash(hash) {
  const [vue, id] = String(hash).replace(/^#/, '').split('/');
  return { vue, id: FORME_ID.test(id || '') ? id : null };
}

const memoriser = (cle, valeur) => { try { localStorage.setItem(cle, valeur); } catch { return; } };

export function transmettre(vue, id) {
  const chargee = !!cadre(vue)?.getAttribute('src');
  if (vue === 'room') {
    memoriser('mu-canal', id);
    if (chargee) cadre(vue).contentWindow.postMessage({ type: 'room', id, entrer: true }, location.origin);
  } else if (vue === 'playlists') {
    if (chargee) cadre(vue).contentWindow.postMessage({ type: 'ouvrir', id }, location.origin);
    else memoriser('mu-dossier', id);
  }
}
