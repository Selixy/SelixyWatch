import { emettre } from '../evenements.js';
import { creerPiste } from './piste.js';
import { lireInformations } from './reseau.js';

const AVANCE = 40;
const ECHECS_MAX = 4;

export function demarrerFlux(video, id) {
  const Source = window.ManagedMediaSource || window.MediaSource;
  if (!Source) { setTimeout(() => emettre('flux-erreur'), 0); return { url: '', arreter() {} }; }
  if (Source === window.ManagedMediaSource) video.disableRemotePlayback = true;
  const source = new Source();
  const url = URL.createObjectURL(source);
  let pistes = [], minuterie = null, actif = true, pompe = false, echecs = 0;
  const pomper = async () => {
    if (!actif || pompe || !pistes.length) return;
    pompe = true;
    try {
      for (const p of pistes) await p.assurer(video.currentTime, AVANCE);
      if (pistes.every((p) => p.fini()) && source.readyState === 'open') source.endOfStream();
      echecs = 0;
    } catch { if (++echecs >= ECHECS_MAX && actif) emettre('flux-erreur'); }
    pompe = false;
  };
  const ouvrir = async () => {
    try {
      const infos = await lireInformations(id);
      if (!Source.isTypeSupported(infos.video.mime) || !Source.isTypeSupported(infos.audio.mime)) throw new Error('format non pris en charge');
      pistes = ['video', 'audio'].map((nom) => creerPiste(source.addSourceBuffer(infos[nom].mime), `/flux/${id}/${nom}`));
      await Promise.all(pistes.map((p) => p.preparer()));
      source.duration = infos.duree;
      minuterie = setInterval(pomper, 500);
      pomper();
    } catch { if (actif) emettre('flux-erreur'); }
  };
  source.addEventListener('sourceopen', ouvrir, { once: true });
  for (const nom of ['seeking', 'waiting']) video.addEventListener(nom, pomper);
  return {
    url,
    arreter() {
      actif = false;
      clearInterval(minuterie);
      for (const nom of ['seeking', 'waiting']) video.removeEventListener(nom, pomper);
      URL.revokeObjectURL(url);
    },
  };
}
