import { S } from './partage.js';
import { notifier } from './observateur.js';

export function messagesDuFlux(relireBibliotheque) {
  return {
    bibliotheque: () => relireBibliotheque(),
    canaux: (d) => { S.canaux = d; notifier('canal'); },
    canal: ({ id, etat }) => { S.canaux[id] = etat; notifier(id === S.canal ? 'canal' : 'autre-canal'); },
    import: ({ playlist, en_cours, erreur }) => { S.imports[playlist] = { en_cours, erreur }; notifier('import'); },
    presence: (d) => { S.presence = d; notifier('presence'); },
  };
}
