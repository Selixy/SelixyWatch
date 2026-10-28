const abonnes = new Map();

export const sur = (nom, f) => {
  if (!abonnes.has(nom)) abonnes.set(nom, []);
  abonnes.get(nom).push(f);
};

export const emettre = (nom, ...args) => {
  for (const f of abonnes.get(nom) ?? []) f(...args);
};
