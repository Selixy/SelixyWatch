import { P } from './page.js';
import { lienReconnu } from './liens.js';

export const avecFichiers = (e) => [...(e.dataTransfer?.types || [])].includes('Files');

export const avecTexte = (e) => !P.glisse && !P.piste && !avecFichiers(e) && [...(e.dataTransfer?.types || [])].some((t) => t === 'text/uri-list' || t === 'text/plain');

export function lienDepose(e) {
  const liste = (e.dataTransfer.getData('text/uri-list') || '').split('\n').map((x) => x.trim()).find((x) => x && !x.startsWith('#'));
  const t = liste || (e.dataTransfer.getData('text/plain') || '').trim();
  return lienReconnu(t) ? t : null;
}
