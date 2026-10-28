import { S } from './partage.js';
import { diffuser } from './observateur.js';
import { messagesDuFlux } from './messages.js';
import { creerRelecture } from './bibliotheque.js';

const EVENEMENTS_DE_ROOM = ['chat', 'reaction', 'signal'];
const lecture = creerRelecture(() => connecter());
const gestionnaires = messagesDuFlux(lecture.demander);
let flux = null;

export function connecter(avecCanal = true) {
  flux?.close();
  flux = new EventSource((avecCanal && S.canal) ? `/api/flux?canal=${encodeURIComponent(S.canal)}` : '/api/flux');
  flux.addEventListener('open', () => lecture.lire());
  for (const [nom, traiter] of Object.entries(gestionnaires)) flux.addEventListener(nom, (m) => traiter(JSON.parse(m.data)));
  for (const nom of EVENEMENTS_DE_ROOM) flux.addEventListener(nom, (m) => diffuser(nom, JSON.parse(m.data)));
}
