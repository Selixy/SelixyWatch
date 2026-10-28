import { vocal } from './etat.js';
import { signaler } from './signal.js';
import { creerPC } from './pairs.js';

export async function surOffre(msg) {
  try {
    const pc = creerPC(msg.de);
    await pc.setRemoteDescription(new RTCSessionDescription(msg.data));
    const reponse = await pc.createAnswer();
    await pc.setLocalDescription(reponse);
    signaler('answer', reponse, msg.de);
  } catch (e) {
    console.warn('Erreur WebRTC offer:', e);
  }
}

export async function surReponse(msg) {
  const pc = vocal.connexions.get(msg.de);
  if (pc) {
    try { await pc.setRemoteDescription(new RTCSessionDescription(msg.data)); } catch (e) {}
  }
}

export async function surCandidat(msg) {
  const pc = vocal.connexions.get(msg.de);
  if (pc && msg.data) {
    try { await pc.addIceCandidate(new RTCIceCandidate(msg.data)); } catch (e) {}
  }
}
