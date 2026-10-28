import { vocal } from './etat.js';
import { mettreAJourPresent } from './affichage.js';
import { calculerAudio } from './volume-calcul.js';
import { estMuet } from '../son/reglage.js';
import { volumeMaitre } from '../son/volume-maitre.js';

export function appliquerAudio(peerId) {
  const audio = vocal.audiosDistants.get(peerId);
  if (!audio) return;
  const { volume, muet } = calculerAudio({
    individuel: vocal.volumesLocaux.get(peerId) ?? 1,
    muetIndividuel: vocal.mutesLocaux.has(peerId),
    maitre: volumeMaitre(),
    muetMaitre: estMuet(),
  });
  audio.volume = volume;
  audio.muted = muet;
}

export function appliquerVolumes() {
  for (const peerId of vocal.audiosDistants.keys()) appliquerAudio(peerId);
}

export function reglerVolumePair(peerId, volume) {
  const vol = Math.max(0, Math.min(1, volume));
  vocal.volumesLocaux.set(peerId, vol);
  if (vol === 0) vocal.mutesLocaux.add(peerId); else vocal.mutesLocaux.delete(peerId);
  appliquerAudio(peerId);
  mettreAJourPresent(peerId);
}

export function basculerMutePair(peerId) {
  if (vocal.mutesLocaux.has(peerId)) {
    vocal.mutesLocaux.delete(peerId);
    if ((vocal.volumesLocaux.get(peerId) ?? 1) === 0) vocal.volumesLocaux.set(peerId, 1);
  } else {
    vocal.mutesLocaux.add(peerId);
  }
  appliquerAudio(peerId);
  mettreAJourPresent(peerId);
}
