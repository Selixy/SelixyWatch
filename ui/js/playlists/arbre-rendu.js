import { esc, icone, avatar } from '../ui.js';
import { S, noeud, enfants, peutDeplacer, estRacineRecue } from '../etat.js';
import { conteneur } from './elements.js';
import { P } from './page.js';
import { ouverts } from './stockage.js';
import { commencerRenommage } from './actions-arbre.js';
import { boutonsLigne } from './arbre-boutons.js';

function presents(id) {
  const l = S.presence?.canaux?.[id] || [];
  return l.length ? `<span class="presents">${l.map((m) => avatar(m, 18)).join('')}</span>` : '';
}

const proprietaire = (n) => (estRacineRecue(n)
  ? `<span class="proprio" title="Partagé par ${esc(n.proprietaire?.pseudo)}">${avatar(n.proprietaire, 18)}</span>`
  : '');

export function ligne(n, niveau) {
  const dossier = n.type === 'dossier';
  const ouvert = ouverts.has(n.id);
  const cls = ['ligne', dossier ? 'dossier' : 'playlist'];
  if (P.selection === n.id) cls.push('select');
  if (!dossier && P.vue === n.id) cls.push('vue-courante');
  if (!dossier && S.canal === n.id) cls.push('ecoute');
  const sous = dossier && ouvert ? `<ul>${enfants(n.id).map((x) => `<li>${ligne(x, niveau + 1)}</li>`).join('')}</ul>` : '';
  const nom = P.edition === n.id
    ? `<input class="nom-edition" value="${esc(n.nom)}" maxlength="${dossier ? 60 : 120}" aria-label="Nom">`
    : `<span class="nom">${esc(n.nom)}</span>`;
  return `<div class="${cls.join(' ')}" data-id="${n.id}" tabindex="0" draggable="${peutDeplacer(n)}" style="--niveau:${niveau}" role="treeitem"` +
    `${dossier ? ` aria-expanded="${ouvert}"` : ''}>` +
    (dossier ? `<span class="chevron${ouvert ? ' ouvert' : ''}" data-a="basculer">${icone('chevron', 14)}</span>` : '<span class="chevron vide"></span>') +
    `<span class="icone">${icone(dossier ? 'dossier' : 'playlist', 16)}</span>${nom}${proprietaire(n)}${dossier ? '' : presents(n.id)}` +
    `${boutonsLigne(n)}</div>${sous}`;
}

export function rendreArbre() {
  conteneur.innerHTML = `<ul class="arbre" role="tree">${enfants('racine').map((n) => `<li>${ligne(n, 0)}</li>`).join('')}</ul>`;
  if (P.aRenommer && noeud(P.aRenommer)) { const id = P.aRenommer; P.aRenommer = null; commencerRenommage(id); }
}
