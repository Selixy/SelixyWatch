import { $ } from '../ui.js';
import { etat, media } from '../etat.js';

export const elements = { video: $('#video'), audio: $('#audio'), ecran: $('#ecran'), salle: $('#salle') };

export const L = {
  actif: null,
  bloque: false,
  premierGeste: 0,
  dernierEssai: 0,
  glisse: null,
  vol: 0.8,
  mut: false,
  dernierGeste: Date.now(),
  doigtPose: false,
  masqueesParToucher: false,
  revelee: 0,
  preparation: { debut: 0, pose: 0, voile: null, fini: false },
};

export const courant = () => media(etat()?.courant);
export const longueur = () => courant()?.duree || L.actif?.duree() || 0;
