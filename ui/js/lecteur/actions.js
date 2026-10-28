import { etat, cible, agir } from '../etat.js';
import { L, courant, longueur } from './contexte.js';
import { erreur } from './messages.js';
import { indiquer } from './indicateur.js';

export const bascule = () => agir(etat()?.courant ? (etat().lecture ? 'pause' : 'lire') : 'lire').catch(erreur);

export function aller(pos) {
  const d = longueur();
  if (!courant()) return;
  const p = Math.max(0, Math.min(d || Infinity, pos));
  L.actif?.aller(p);
  agir('aller', { pos: p }).catch(erreur);
}

export function deplacer(delta) {
  aller(cible() + delta);
  indiquer(`${delta > 0 ? '+' : '−'}${Math.abs(delta)} s`);
}

export const fin = () => {
  const e = etat();
  if (e?.courant) agir('fin', { media: e.courant, v: e.v }).catch(() => {});
};
