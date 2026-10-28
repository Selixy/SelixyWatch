import { S, surChangement, etat, cible, media, nom, agir } from './etat.js';
import { urlMiniature } from './ui.js';

const ms = navigator.mediaSession;
let vu = '';

function maj() {
  const e = etat(), m = media(e?.courant);
  if (!m) { ms.metadata = null; ms.playbackState = 'none'; vu = ''; return; }
  const cle = `${e.courant}|${nom(S.canal)}`;
  if (cle !== vu) {
    vu = cle;
    const u = urlMiniature(e.courant, m);
    ms.metadata = new MediaMetadata({
      title: m.nom, artist: nom(S.canal), album: 'SelixyWatch',
      artwork: u ? [{ src: new URL(u, location.href).href, sizes: '320x180' }] : [],
    });
  }
  ms.playbackState = e.lecture ? 'playing' : 'paused';
  try {
    if (m.duree) ms.setPositionState({ duration: m.duree, position: Math.min(m.duree, Math.max(0, cible(e))), playbackRate: 1 });
  } catch { return; }
}

export function initSession() {
  if (!ms || typeof MediaMetadata === 'undefined') return;
  const rejet = () => {};
  const vers = (nomAction, corps) => () => { agir(nomAction, corps).catch(rejet); };
  const decal = (d) => () => agir('aller', { pos: Math.max(0, cible() + d) }).catch(rejet);
  const actions = {
    play: vers('lire'), pause: vers('pause'),
    previoustrack: vers('precedent'), nexttrack: vers('suivant'),
    seekbackward: decal(-10), seekforward: decal(10),
    seekto: (d) => { if (d.seekTime != null) agir('aller', { pos: Math.max(0, d.seekTime) }).catch(rejet); },
  };
  for (const [a, f] of Object.entries(actions)) { try { ms.setActionHandler(a, f); } catch { continue; } }
  surChangement(maj);
  maj();
}
