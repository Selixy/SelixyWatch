import { api } from '../api.js';
import { S } from './partage.js';

const MESURES = 6;
const PAUSE_MS = 120;

export async function etalonner() {
  let meilleur = null;
  for (let i = 0; i < MESURES; i++) {
    const t1 = Date.now() / 1000;
    const r = await api('/api/heure');
    const t2 = Date.now() / 1000;
    if (r.ok && (!meilleur || t2 - t1 < meilleur.rtt)) meilleur = { rtt: t2 - t1, ecart: r.data.t + (t2 - t1) / 2 - t2 };
    await new Promise((ok) => setTimeout(ok, PAUSE_MS));
  }
  if (meilleur) S.decalage = meilleur.ecart;
}
