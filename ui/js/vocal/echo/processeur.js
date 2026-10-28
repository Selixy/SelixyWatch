import { creerAnnuleur } from './annuleur.js';
import { creerPorte } from './porte.js';

class AnnuleurEcho extends AudioWorkletProcessor {
  constructor() {
    super();
    this.annuleur = creerAnnuleur(sampleRate);
    this.porte = creerPorte(sampleRate);
  }

  process(entrees, sorties) {
    const mic = entrees[0][0];
    const ref = entrees[1]?.[0];
    const sortie = sorties[0][0];
    if (!mic) return true;
    for (let i = 0; i < mic.length; i++) sortie[i] = this.porte.traiter(this.annuleur.traiter(mic[i], ref ? ref[i] : 0));
    return true;
  }
}

registerProcessor('annuleur-echo', AnnuleurEcho);
