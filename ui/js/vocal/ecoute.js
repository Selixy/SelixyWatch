import { S, surEvenement } from '../etat.js';
import { vocal } from './etat.js';
import { surInitEtats, surEtat, surDepart } from './signal-etats.js';
import { surOffre, surReponse, surCandidat } from './signal-webrtc.js';

const POUR_MOI = new Set(['offer', 'answer', 'ice']);

const GESTIONNAIRES = {
  init_etats: surInitEtats,
  etat: surEtat,
  offer: surOffre,
  answer: surReponse,
  ice: surCandidat,
  depart: surDepart
};

async function traiter(msg) {
  if (msg.canal !== S.canal) return;
  if (msg.de === vocal.moi?.id) return;
  if (POUR_MOI.has(msg.action) && msg.cible !== vocal.moi?.id) return;
  await GESTIONNAIRES[msg.action]?.(msg);
}

export function ecouterSignaux() {
  surEvenement('signal', traiter);
}
