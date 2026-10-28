import { filtrerMicro } from './echo/index.js';

export const SUPPORTS = {
  micro: {
    genre: 'audio',
    contraintes: { audio: { echoCancellation: true, noiseSuppression: true, autoGainControl: false, suppressLocalAudioPlayback: true, voiceIsolation: true } },
    traiter: (piste) => filtrerMicro(piste, document.querySelectorAll('#video, #audio')),
    erreur: 'Impossible d\'accéder au microphone : '
  },
  camera: {
    genre: 'video',
    contraintes: { video: { width: { ideal: 480 }, height: { ideal: 480 }, aspectRatio: 1 } },
    traiter: async (piste) => piste,
    erreur: 'Impossible d\'accéder à la caméra : '
  }
};
