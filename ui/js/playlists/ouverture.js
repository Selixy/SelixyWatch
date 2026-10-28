import { S, noeud, estPlaylist } from '../etat.js';
import { idsADeplier } from './ouverture-chemin.js';
import { P, message } from './page.js';
import { lire, ecrire, ouverts, sauverOuverts, memoriserVue } from './stockage.js';

const DELAI_MS = 10000;

export function demanderOuverture(id) {
  P.aOuvrir = id;
  P.ouvrirAvant = Date.now() + DELAI_MS;
}

function lireMemorise() {
  const memorise = lire('mu-dossier', '');
  if (!memorise) return;
  ecrire('mu-dossier', '');
  demanderOuverture(memorise);
}

export function ouvrirDemande() {
  lireMemorise();
  const id = P.aOuvrir;
  if (!id || !S.pret) return;
  const n = noeud(id);
  if (!n) {
    if (Date.now() > P.ouvrirAvant) { P.aOuvrir = null; message('Cet élément n\'est plus accessible.'); }
    return;
  }
  P.aOuvrir = null;
  for (const a of idsADeplier(n, noeud)) ouverts.add(a);
  sauverOuverts();
  P.selection = id;
  if (estPlaylist(id)) { P.vue = id; memoriserVue(id); }
}

export function brancherOuverture(rendre) {
  window.addEventListener('message', (e) => {
    if (e.origin !== location.origin || e.data?.type !== 'ouvrir') return;
    demanderOuverture(String(e.data.id));
    rendre();
  });
}
