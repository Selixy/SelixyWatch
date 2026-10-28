import { etat } from '../etat.js';
import { poserVoile, retirerVoile } from '../marque/voile.js';
import { L, elements, courant } from './contexte.js';
import { decider, lecteurEstPret } from './preparation-etapes.js';

const PERIODE_MS = 200;

const estPrete = () => Boolean(etat()) && (!courant() || (L.actif !== null && lecteurEstPret(L.actif, L.bloque)));

function appliquer(action, p, maintenant) {
  if (action === 'demarrer') p.debut = maintenant;
  if (action === 'poser') { p.voile = poserVoile(elements.ecran, '/visuels/preparation.svg'); p.pose = maintenant; }
  if (action === 'retirer') { retirerVoile(p.voile); p.fini = true; }
  if (action === 'terminer') p.fini = true;
}

export function initPreparation() {
  const minuteur = setInterval(() => {
    const maintenant = Date.now();
    appliquer(decider(L.preparation, estPrete(), maintenant), L.preparation, maintenant);
    if (L.preparation.fini) clearInterval(minuteur);
  }, PERIODE_MS);
}
