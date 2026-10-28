import { S, maintenant } from './partage.js';
import { poster } from './requetes.js';

export const etat = (canal = S.canal) => S.canaux[canal];

export function cible(e = etat()) {
  if (!e) return 0;
  return e.lecture ? e.pos + (maintenant() - e.t0) : e.pos;
}

export async function action(canal, nom, corps = {}) {
  await poster(`/api/canal/${canal}/${nom}`, corps);
}

export const agir = (nom, corps) => action(S.canal, nom, corps);
