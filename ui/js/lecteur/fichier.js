import { emettre } from './evenements.js';

const videler = (v) => { v.pause(); if (v.getAttribute('src')) { v.removeAttribute('src'); v.load(); } };

const origineFichier = { url: (id, m) => `/medias/${id}.${m.ext}`, arreter() {} };

export function creerLecteurFichier({ video, audio }, origine = origineFichier) {
  let el = video, dernierSaut = 0;
  return {
    finesse: 0.05,
    charger(id, m) {
      const src = origine.url(id, m), voulu = m.genre === 'audio' ? audio : video;
      if (voulu !== el) { videler(el); el = voulu; emettre('son-a-appliquer'); }
      if (!el.src.endsWith(src)) { el.src = src; el.load(); }
    },
    pret: () => el.readyState >= 1,
    occupe: () => false,
    position: () => el.currentTime,
    duree: () => el.duration || 0,
    aller: (s) => { dernierSaut = Date.now(); el.currentTime = s; },
    recaler(but) {
      const ecart = but - el.currentTime;
      if (Math.abs(ecart) > 2.5) {
        if (Date.now() - dernierSaut > (el.readyState < 3 ? 8000 : 4000)) { dernierSaut = Date.now(); el.currentTime = but; }
        return;
      }
      el.playbackRate = Math.abs(ecart) < 0.15 ? 1 : 1 + Math.max(-0.07, Math.min(0.07, ecart * 0.2));
    },
    jouer: () => el.play(),
    pause: () => { el.playbackRate = 1; el.pause(); },
    estEnPause: () => el.paused,
    volume: (v) => { el.volume = v; },
    muet: (b) => { el.muted = b; },
    vider() { origine.arreter(); videler(video); videler(audio); },
    estElement: (v) => v === el,
    reinitialiser: () => { dernierSaut = 0; },
  };
}
