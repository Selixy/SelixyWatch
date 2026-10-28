import { etat, cible, agir } from '../etat.js';
import { L, elements, courant } from './contexte.js';
import { lecteurs, lecteurDe, yt } from './fabrique.js';
import { sur } from './evenements.js';
import { message } from './messages.js';
import { fin } from './actions.js';
import { appliquerSon } from './volume.js';
import { majPoster } from './poster.js';
import { signaler, lire } from './deblocage.js';
import { surveillerPub } from './youtube-pub.js';
import { tic } from './progression.js';

export function caler() {
  const m = courant(), e = etat();
  const l = lecteurDe(m);
  if (l !== L.actif) {
    L.actif?.vider();
    L.actif = l;
    elements.ecran.classList.toggle('yt', l === yt);
    signaler(false);
  }
  if (!l) return;
  l.charger(e.courant, m, e);
  if (!l.pret() || l.occupe()) return;
  const but = cible(e);
  if (e.lecture) {
    if (but >= (l.duree() || m.duree || Infinity)) return;
    l.recaler(but);
    if (l.estEnPause() && (!L.bloque || Date.now() - L.dernierEssai > 2500)) { L.dernierEssai = Date.now(); lire(l); }
  } else {
    l.pause();
    if (Math.abs(l.position() - e.pos) > l.finesse) { l.aller(e.pos); l.pause(); }
  }
}

function surEtatYoutube(ev) {
  if (L.actif !== yt) return;
  if (ev.data === 0 && yt.charge === yt.voulu && !yt.enPub) fin();
  caler();
}

function surErreurYoutube(ev) {
  if (L.actif !== yt) return;
  const definitive = [100, 101, 150].includes(ev.data);
  message(definitive ? 'Cette vidéo YouTube ne peut pas être lue ici, passage à la suite.' : 'Erreur du lecteur YouTube.');
  if (definitive) fin();
}

function surErreurFlux() {
  message('Cette vidéo YouTube n\'est pas disponible pour le moment : lecture en pause.');
  if (etat()?.lecture) agir('pause').catch(() => {});
}

export function initSynchro() {
  sur('yt-pret', () => { appliquerSon(); caler(); });
  sur('yt-etat', surEtatYoutube);
  sur('yt-erreur', surErreurYoutube);
  sur('pub-finie', caler);
  sur('flux-erreur', surErreurFlux);
  for (const v of [elements.video, elements.audio]) {
    v.addEventListener('loadedmetadata', () => { if (L.actif?.estElement?.(v)) { tic(); caler(); } });
    v.addEventListener('canplay', () => { if (L.actif?.estElement?.(v)) caler(); });
    v.addEventListener('ended', () => { if (L.actif?.estElement?.(v)) fin(); });
  }
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) return;
    for (const l of lecteurs) l.reinitialiser();
    L.dernierEssai = 0;
    caler(); majPoster();
  });
  setInterval(() => { if (etat()?.lecture && L.actif && !L.actif.estEnPause()) caler(); }, 1000);
  setInterval(surveillerPub, 500);
}
