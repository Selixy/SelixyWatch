import { $ } from '../ui.js';
import { surChangement } from '../etat.js';
import { moi } from '../compte.js';
import { initVocal, ouvrirMenuProfil } from '../vocal.js';
import { initReactions } from './reactions.js';
import { rendre } from './liste.js';

export async function initPresence() {
  initReactions();
  await initVocal();
  const me = await moi();
  $('#reagir').hidden = !me;
  $('#presents').addEventListener('click', (e) => {
    const p = e.target.closest('.present');
    if (!p) return;
    ouvrirMenuProfil(p.dataset.id, p);
  });
  rendre(me);
  surChangement((quoi) => { if (quoi === 'presence' || quoi === 'arbre') rendre(me); });
}
