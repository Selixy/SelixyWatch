import { vocal, monEtat } from './etat.js';
import { mettreAJourPresent } from './affichage.js';
import { appeler, fermerPC } from './pairs.js';

export function surInitEtats(msg) {
  for (const [id, etat] of Object.entries(msg.etats || {})) {
    vocal.etatsPairs.set(id, etat);
    mettreAJourPresent(id);
  }
}

export async function surEtat(msg) {
  vocal.etatsPairs.set(msg.de, msg.data || { micro: false, camera: false });
  mettreAJourPresent(msg.de);
  if (monEtat.micro || monEtat.camera || msg.data?.micro || msg.data?.camera) {
    if (vocal.moi?.id && vocal.moi.id > msg.de) {
      try { await appeler(msg.de); } catch (e) {}
    }
  }
}

export function surDepart(msg) {
  fermerPC(msg.de);
  vocal.etatsPairs.delete(msg.de);
  mettreAJourPresent(msg.de);
}
