const abonnes = new Set();
const evenements = {};

export const surEvenement = (nom, f) => (evenements[nom] ||= new Set()).add(f);
export const surChangement = (f) => abonnes.add(f);
export const notifier = (quoi) => abonnes.forEach((f) => f(quoi));
export const diffuser = (nom, donnee) => evenements[nom]?.forEach((f) => f(donnee));
