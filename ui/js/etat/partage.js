import { lire } from './stockage.js';

export const S = {
  noeuds: [],
  medias: {},
  canaux: {},
  imports: {},
  presence: { canaux: {} },
  canal: lire('mu-canal', '') || null,
  decalage: 0,
  pret: false,
  anonyme: false,
  refuse: false,
};

export const maintenant = () => Date.now() / 1000 + S.decalage;
