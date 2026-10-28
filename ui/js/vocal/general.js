import { vocal, monEtat } from './etat.js';
import { basculerMicro } from './medias.js';
import { appliquerVolumes } from './volume.js';
import { estMuet, estCleMuet } from '../son/reglage.js';
import { estCleVolume } from '../son/volume-maitre.js';

async function surChangement() {
  appliquerVolumes();
  const muet = estMuet();
  if (muet === vocal.muetAvant) return;
  vocal.muetAvant = muet;
  if (muet && monEtat.micro) {
    vocal.microAvantCoupure = true;
    await basculerMicro();
  } else if (!muet && vocal.microAvantCoupure) {
    vocal.microAvantCoupure = false;
    if (!monEtat.micro) await basculerMicro();
  }
}

export function initSonGeneral() {
  vocal.muetAvant = estMuet();
  window.addEventListener('son-local', surChangement);
  window.addEventListener('storage', (e) => { if (estCleMuet(e.key) || estCleVolume(e.key)) surChangement(); });
}
