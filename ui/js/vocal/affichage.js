import { vocal, estMoi, etatDe } from './etat.js';
import { ajusterTaillesPresents } from './taille.js';

function majVideo(el, id, etat) {
  let video = el.querySelector('.avatar-video');
  if (!etat.camera) {
    video?.remove();
    return;
  }
  if (!video) {
    video = document.createElement('video');
    video.className = 'avatar-video';
    video.autoplay = true;
    video.playsInline = true;
    video.muted = true;
    el.prepend(video);
  }
  const flux = estMoi(id) ? vocal.flux : vocal.fluxDistants.get(id);
  if (flux && video.srcObject !== flux) video.srcObject = flux;
}

function majBadge(el, muet, etat) {
  let badge = el.querySelector('.badge-vocal');
  const aspect = muet ? ['mute', 'Son coupé pour vous'] : (etat.micro ? ['actif', 'Micro actif'] : null);
  if (!aspect) {
    badge?.remove();
    return;
  }
  if (!badge) {
    badge = document.createElement('span');
    el.appendChild(badge);
  }
  badge.className = `badge-vocal ${aspect[0]}`;
  badge.textContent = '';
  badge.title = aspect[1];
}

export function mettreAJourPresent(peerId) {
  const zone = document.getElementById('presents');
  if (!zone) return;
  const el = zone.querySelector(`.present[data-id="${peerId}"]`);
  if (!el) return;

  const etat = etatDe(peerId);
  const muet = vocal.mutesLocaux.has(peerId);
  el.classList.toggle('avec-video', !!etat.camera);
  el.classList.toggle('avec-micro', !!etat.micro);
  el.classList.toggle('muet-local', muet);
  majVideo(el, peerId, etat);
  majBadge(el, muet, etat);
  ajusterTaillesPresents();
}

export function synchroniserVocalTous() {
  if (vocal.moi?.id) mettreAJourPresent(vocal.moi.id);
  for (const peerId of vocal.etatsPairs.keys()) {
    mettreAJourPresent(peerId);
  }
  ajusterTaillesPresents();
}
