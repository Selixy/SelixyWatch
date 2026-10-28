import { vocal, monEtat } from './etat.js';
import { signaler } from './signal.js';
import { mettreAJourPresent } from './affichage.js';
import { connecterAvecPairs } from './pairs.js';
import { suivreVoix, oublierVoix } from './voix.js';
import { SUPPORTS } from './supports.js';

async function activer(nom) {
  const { genre, contraintes, traiter, erreur } = SUPPORTS[nom];
  try {
    const flux = await navigator.mediaDevices.getUserMedia(contraintes);
    const piste = await traiter(flux.getTracks().find((p) => p.kind === genre));
    if (!vocal.flux) {
      vocal.flux = new MediaStream([piste]);
    } else {
      vocal.flux.addTrack(piste);
    }
    for (const pc of vocal.connexions.values()) {
      pc.addTrack(piste, vocal.flux);
    }
    monEtat[nom] = true;
    if (nom === 'micro') suivreVoix(vocal.moi.id, piste);
    signaler('etat', monEtat);
    mettreAJourPresent(vocal.moi.id);
    await connecterAvecPairs();
  } catch (e) {
    alert(erreur + (e.message || e.name));
  }
}

function couper(nom) {
  const { genre } = SUPPORTS[nom];
  if (vocal.flux) {
    for (const piste of vocal.flux.getTracks().filter((p) => p.kind === genre)) {
      piste.stop();
      vocal.flux.removeTrack(piste);
      for (const pc of vocal.connexions.values()) {
        const emetteur = pc.getSenders().find((s) => s.track === piste);
        if (emetteur) pc.removeTrack(emetteur);
      }
    }
  }
  monEtat[nom] = false;
  if (nom === 'micro') oublierVoix(vocal.moi.id);
  signaler('etat', monEtat);
  mettreAJourPresent(vocal.moi.id);
}

async function basculer(nom) {
  if (!vocal.moi?.id) return;
  if (!monEtat[nom]) await activer(nom);
  else couper(nom);
}

export const basculerMicro = () => basculer('micro');

export const basculerCamera = () => basculer('camera');
