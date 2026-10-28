import { $ } from '../ui.js';
import { S, poster, noeud } from '../etat.js';
import { lienComplet, copier } from './lien.js';
import { htmlLien, htmlContenu } from './rendu.js';
import { htmlInviter, htmlArbreCases } from './rendu-inviter.js';
import { ouvrirFenetre, fermer } from './fenetre.js';
import { hauts } from './selection.js';
import { estMien, mesNoeuds, basculer } from './propres.js';

let voile = null;
let coches = new Set();
let lien = '';
const dire = (texte) => { $('.message', voile).textContent = texte || ''; };
const afficherArbre = () => { $('#partage-arbre', voile).innerHTML = htmlArbreCases(S.noeuds, coches); };

async function creer(form) {
  const ids = hauts(mesNoeuds(S.noeuds), coches);
  if (!ids.length) return dire('Cochez au moins un élément.');
  const f = new FormData(form);
  try {
    const r = await poster('/api/invitations', { noeuds: ids, usages_max: Number(f.get('usages')), jours: Number(f.get('jours')), pro: !!$('input[name=pro]', voile)?.checked });
    lien = lienComplet(location.origin, r.lien);
    $('#partage-nouveau', voile).innerHTML = htmlLien(lien) + `<h3>Partagé par ce lien${r.pro ? ' (offre aussi le statut Pro)' : ''}</h3>` + htmlContenu(r.noeuds);
    dire('');
  } catch (e) { dire(e.message); }
}

async function surClic(e) {
  const b = e.target.closest('[data-a]');
  if (e.target === voile || b?.dataset.a === 'fermer') return fermer();
  if (b?.dataset.a === 'copier') dire(await copier(lien) ? 'Lien copié.' : 'Copie impossible : sélectionnez le lien.');
}

export async function ouvrirInviter(preselection) {
  const admin = await fetch('/api/moi').then((r) => r.json()).then((m) => !!m.admin).catch(() => false);
  coches = new Set(estMien(noeud(preselection)) ? [preselection] : []);
  lien = '';
  voile = ouvrirFenetre('Inviter', htmlInviter(S.noeuds, coches, admin));
  voile.addEventListener('click', surClic);
  voile.addEventListener('change', (e) => {
    if (!e.target.dataset?.id) return;
    coches = basculer(coches, e.target.dataset.id, e.target.checked);
    afficherArbre();
  });
  voile.addEventListener('submit', (e) => { e.preventDefault(); creer(e.target); });
}
