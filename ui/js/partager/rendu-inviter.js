import { esc } from '../ui.js';
import { couverts } from './selection.js';
import { mesNoeuds } from './propres.js';

function htmlCase(n, ctx, niveau) {
  const grise = ctx.couvert.has(n.id);
  const coche = grise || ctx.coches.has(n.id);
  const sous = ctx.mien.filter((x) => x.parent === n.id).map((x) => htmlCase(x, ctx, niveau + 1)).join('');
  return `<label class="partage-case" style="--niveau:${niveau}"><input type="checkbox" data-id="${esc(n.id)}"${coche ? ' checked' : ''}${grise ? ' disabled' : ''}>` +
    `<span class="nom">${esc(n.nom)}</span><span class="note">${n.type === 'dossier' ? 'Dossier' : 'Playlist'}</span></label>${sous}`;
}

export function htmlArbreCases(noeuds, coches) {
  const mien = mesNoeuds(noeuds);
  const ctx = { mien, coches, couvert: couverts(mien, coches) };
  const racines = mien.filter((n) => !mien.some((x) => x.id === n.parent));
  return racines.length
    ? `<div class="partage-arbre">${racines.map((n) => htmlCase(n, ctx, 0)).join('')}</div>`
    : '<p class="note">Vous n\'avez encore rien à partager.</p>';
}

const htmlCasePro = (admin) => admin
  ? '<label class="partage-case"><input type="checkbox" name="pro"><span class="nom">Offrir aussi le statut Pro</span></label>'
  : '';

export const htmlFormulaire = (admin) =>
  htmlCasePro(admin) + '<form class="partage-form" id="partage-form"><label>Usages<input type="number" name="usages" min="1" max="50" value="5"></label>' +
  '<label>Durée (jours)<input type="number" name="jours" min="1" max="30" value="7"></label>' +
  '<button type="submit" class="bouton principal">Créer le lien</button></form>';

export const htmlInviter = (noeuds, coches, admin) =>
  `<p class="note">Cochez ce que vous partagez : un dossier coché couvre son contenu.</p><div id="partage-arbre">${htmlArbreCases(noeuds, coches)}</div>` +
  `${htmlFormulaire(admin)}<div id="partage-nouveau"></div>`;
