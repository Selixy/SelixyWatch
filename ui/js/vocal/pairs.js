import { vocal, monEtat } from './etat.js';
import { signaler } from './signal.js';
import { mettreAJourPresent } from './affichage.js';
import { suivreVoix, oublierVoix } from './voix.js';
import { appliquerAudio } from './volume.js';

const RTC_CONFIG = {
  iceServers: [
    { urls: 'stun:stun.l.google.com:19302' },
    { urls: 'stun:stun1.l.google.com:19302' }
  ]
};

export function fermerPC(peerId) {
  const pc = vocal.connexions.get(peerId);
  if (pc) {
    try { pc.close(); } catch (e) {}
    vocal.connexions.delete(peerId);
  }
  const audio = vocal.audiosDistants.get(peerId);
  if (audio) {
    audio.remove();
    vocal.audiosDistants.delete(peerId);
  }
  vocal.fluxDistants.delete(peerId);
  oublierVoix(peerId);
}

function recevoirPiste(peerId, piste) {
  let flux = vocal.fluxDistants.get(peerId);
  if (!flux) {
    flux = new MediaStream();
    vocal.fluxDistants.set(peerId, flux);
  }
  flux.addTrack(piste);

  if (piste.kind === 'video') {
    mettreAJourPresent(peerId);
    return;
  }
  if (piste.kind !== 'audio') return;
  let audio = vocal.audiosDistants.get(peerId);
  if (!audio) {
    audio = document.createElement('audio');
    audio.autoplay = true;
    audio.style.display = 'none';
    document.body.appendChild(audio);
    vocal.audiosDistants.set(peerId, audio);
  }
  audio.srcObject = flux;
  appliquerAudio(peerId);
  suivreVoix(peerId, piste);
}

export function creerPC(peerId) {
  if (vocal.connexions.has(peerId)) return vocal.connexions.get(peerId);
  const pc = new RTCPeerConnection(RTC_CONFIG);
  vocal.connexions.set(peerId, pc);

  if (vocal.flux) {
    for (const piste of vocal.flux.getTracks()) {
      pc.addTrack(piste, vocal.flux);
    }
  }
  pc.onicecandidate = (e) => {
    if (e.candidate) signaler('ice', e.candidate, peerId);
  };
  pc.ontrack = (e) => recevoirPiste(peerId, e.track);
  pc.onconnectionstatechange = () => {
    if (pc.connectionState === 'failed' || pc.connectionState === 'closed') {
      fermerPC(peerId);
    }
  };
  return pc;
}

export async function appeler(peerId) {
  const pc = creerPC(peerId);
  const offre = await pc.createOffer();
  await pc.setLocalDescription(offre);
  signaler('offer', offre, peerId);
}

export async function connecterAvecPairs() {
  const moiId = vocal.moi?.id;
  if (!moiId) return;
  for (const [peerId, etat] of vocal.etatsPairs.entries()) {
    if (peerId === moiId) continue;
    if (moiId > peerId && (monEtat.micro || monEtat.camera || etat.micro || etat.camera)) {
      try { await appeler(peerId); } catch (e) {}
    }
  }
}
