import { ajouter, retirer } from './tampon.js';
import { finTamponnee, debutTamponne } from './plages.js';
import { segmentApres, tamponComplet } from './segments.js';
import { lireIndex } from './index.js';
import { lireOctets } from './reseau.js';

const MARGE_ARRIERE = 20;

export function creerPiste(tampon, adresse, lire = lireOctets) {
  let segments = [];
  const piste = {
    async preparer() {
      const index = await lireIndex(adresse, lire);
      segments = index.segments;
      await ajouter(tampon, index.init);
    },
    async assurer(t, avance) {
      let fin = finTamponnee(tampon, t);
      let k = segmentApres(segments, fin ?? t);
      while (k >= 0 && k < segments.length && (fin ?? t) < t + avance) {
        const s = segments[k++];
        await ajouter(tampon, await lire(adresse, s.octet, s.octet + s.taille - 1));
        fin = finTamponnee(tampon, t) ?? s.fin;
      }
      await piste.elaguer(t);
    },
    async elaguer(t) {
      const debut = debutTamponne(tampon);
      if (debut !== null && debut < t - MARGE_ARRIERE - 5) await retirer(tampon, 0, t - MARGE_ARRIERE);
    },
    fini: () => tamponComplet(tampon, segments),
  };
  return piste;
}
