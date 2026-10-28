import { etat } from '../etat.js';
import { L, elements, courant } from './contexte.js';
import { yt } from './fabrique.js';
import { emettre } from './evenements.js';

function devinerPub(e, m) {
  if (!e?.lecture || !m || !yt.ok) return false;
  const id = yt.lecteur.getVideoData?.()?.video_id, d = yt.lecteur.getDuration();
  if (id && id !== yt.voulu) return true;
  if (m.duree && d > 0 && Math.abs(d - m.duree) > Math.max(3, m.duree * 0.02)) return true;
  return false;
}

export function surveillerPub() {
  if (L.actif !== yt || !yt.pret()) return;
  const pub = devinerPub(etat(), courant());
  if (pub === yt.enPub) return;
  yt.enPub = pub;
  elements.ecran.classList.toggle('pub', pub);
  if (!pub) { yt.dernierSaut = null; emettre('pub-finie'); }
}
