import { S, noeud } from '../etat.js';
import { page } from './elements.js';
import { P } from './page.js';
import { rendreArbre } from './arbre-rendu.js';
import { rendreVue } from './vue-pistes.js';
import { ouvrirDemande } from './ouverture.js';

export function rendrePage() {
  page.classList.toggle('anonyme', S.anonyme);
  if (S.anonyme) return;
  if (P.glisse || P.piste || P.edition) { P.enAttente = true; return; }
  P.enAttente = false;
  ouvrirDemande();
  if (P.selection !== 'racine' && !noeud(P.selection)) P.selection = 'racine';
  rendreArbre();
  rendreVue();
}
