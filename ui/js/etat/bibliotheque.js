import { api } from '../api.js';
import { S } from './partage.js';
import { estPlaylist } from './arbre.js';
import { notifier } from './observateur.js';
import { effacer } from './stockage.js';
import { lireReponse } from './construction.js';
import { regrouper } from './regroupement.js';

export function creerRelecture(reconnecter) {
  async function lire() {
    const r = await api('/api/bibliotheque');
    const lu = lireReponse(r.status, r.data);
    if (!lu) return;
    Object.assign(S, { anonyme: lu.anonyme, noeuds: lu.noeuds, medias: lu.medias, pret: true });
    if (S.canal && !lu.anonyme && !estPlaylist(S.canal)) {
      S.canal = null;
      S.refuse = true;
      effacer('mu-canal');
      reconnecter();
    }
    notifier('arbre');
  }
  return { lire, demander: regrouper(lire) };
}
