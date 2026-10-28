export const monEtat = { micro: false, camera: false };

export const vocal = {
  moi: null,
  flux: null,
  menu: null,
  etatsPairs: new Map(),
  connexions: new Map(),
  fluxDistants: new Map(),
  audiosDistants: new Map(),
  mutesLocaux: new Set(),
  volumesLocaux: new Map(),
  microAvantCoupure: false,
  muetAvant: false
};

export const estMoi = (id) => !!vocal.moi && id === vocal.moi.id;

export const etatDe = (id) => (estMoi(id) ? monEtat : (vocal.etatsPairs.get(id) || { micro: false, camera: false }));
