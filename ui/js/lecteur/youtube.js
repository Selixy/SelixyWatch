import { cible } from '../etat.js';
import { construireLecteur } from './youtube-api.js';
import { attendreLecture, arreter } from './youtube-lecture.js';

export function creerLecteurYoutube(ecran) {
  const yt = {
    finesse: 1.5,
    lecteur: null, creation: null, ok: false,
    voulu: null, charge: null,
    enPub: false, enCours: null,
    dernierSaut: null,
    dernierRecalage: 0,
    etat: () => (yt.ok && yt.lecteur ? yt.lecteur.getPlayerState() : -1),
    charger(id, m, e) {
      yt.voulu = m.yt;
      if (!yt.lecteur && !yt.creation) yt.creation = construireLecteur(yt, e);
      if (yt.ok && yt.charge !== yt.voulu) {
        yt.charge = yt.voulu; yt.enPub = false; yt.dernierSaut = null; yt.dernierRecalage = Date.now();
        const o = { videoId: yt.voulu, startSeconds: e.lecture ? cible(e) : e.pos };
        if (e.lecture) yt.lecteur.loadVideoById(o); else yt.lecteur.cueVideoById(o);
      }
    },
    pret: () => yt.ok && yt.charge === yt.voulu,
    preparee: () => yt.ok && yt.charge === yt.voulu && [1, 2, 5].includes(yt.etat()),
    occupe: () => yt.enPub,
    position: () => (yt.ok && yt.lecteur ? yt.lecteur.getCurrentTime() : 0) || 0,
    duree: () => (yt.ok && yt.lecteur?.getDuration()) || 0,
    aller(s) {
      if (yt.dernierSaut && Math.abs(yt.dernierSaut.but - s) < 0.2 && Date.now() - yt.dernierSaut.a < 2000) return;
      yt.dernierRecalage = Date.now();
      yt.dernierSaut = { but: s, a: Date.now() };
      if (yt.ok) yt.lecteur.seekTo(s, true);
    },
    recaler(but) {
      const ecart = Math.abs(yt.position() - but);
      if (ecart > 1.2 && (ecart > 2.5 || Date.now() - yt.dernierRecalage > 3000)) {
        yt.dernierRecalage = Date.now();
        yt.aller(but);
      }
    },
    jouer: () => attendreLecture(yt),
    pause: () => { if (yt.ok && [1, 3, -1, 5].includes(yt.etat())) yt.lecteur.pauseVideo(); },
    estEnPause: () => ![1, 3].includes(yt.etat()),
    volume: (v) => { if (yt.ok) yt.lecteur.setVolume(Math.round(v * 100)); },
    muet: (b) => { if (yt.ok) b ? yt.lecteur.mute() : yt.lecteur.unMute(); },
    vider() {
      if (yt.ok) arreter(yt.lecteur);
      yt.voulu = yt.charge = null; yt.enPub = false; yt.dernierSaut = null;
      ecran.classList.remove('pub');
    },
    reinitialiser: () => { yt.dernierRecalage = 0; },
  };
  return yt;
}
