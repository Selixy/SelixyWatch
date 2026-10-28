import { message } from './messages.js';
import { emettre } from './evenements.js';
import { cible } from '../etat.js';

let promesseAPI = null;

function chargerAPI() {
  promesseAPI ??= new Promise((ok, ko) => {
    if (window.YT?.Player) return ok();
    const avant = window.onYouTubeIframeAPIReady;
    window.onYouTubeIframeAPIReady = () => { avant?.(); ok(); };
    const s = document.createElement('script');
    s.src = 'https://www.youtube.com/iframe_api';
    s.onerror = () => { promesseAPI = null; ko(new Error('YouTube est inaccessible')); };
    document.head.append(s);
  });
  return promesseAPI;
}

export function construireLecteur(yt, e) {
  const depart = yt.voulu;
  return chargerAPI().then(() => {
    yt.lecteur = new YT.Player('yt-hote', {
      host: 'https://www.youtube-nocookie.com', width: '100%', height: '100%', videoId: depart,
      playerVars: {
        controls: 0, disablekb: 1, fs: 0, rel: 0, iv_load_policy: 3, cc_load_policy: 0, playsinline: 1, modestbranding: 1,
        autoplay: e.lecture ? 1 : 0, start: Math.floor(cible(e)), origin: location.origin,
      },
      events: {
        onReady: () => { yt.ok = true; yt.charge = depart; emettre('yt-pret'); },
        onStateChange: (ev) => emettre('yt-etat', ev),
        onError: (ev) => emettre('yt-erreur', ev),
      },
    });
  }).catch((err) => { yt.creation = null; message(err.message); });
}
