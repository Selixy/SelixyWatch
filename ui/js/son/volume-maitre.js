import { fixerMuet } from './reglage.js';

const CLE_VOLUME = 'mu-volume';
const VOLUME_DEFAUT = 0.8;

export function volumeMaitre() {
  try {
    const v = Number(localStorage.getItem(CLE_VOLUME) ?? VOLUME_DEFAUT);
    return Number.isFinite(v) ? Math.max(0, Math.min(1, v)) : VOLUME_DEFAUT;
  } catch { return VOLUME_DEFAUT; }
}

export function fixerVolumeMaitre(v) {
  try { localStorage.setItem(CLE_VOLUME, String(Math.max(0, Math.min(1, v)))); } catch { return; }
  fixerMuet(false);
}

export const estCleVolume = (cle) => cle === CLE_VOLUME;
