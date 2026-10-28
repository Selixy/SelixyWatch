import { $, esc, duree, icone, vignette } from '../ui.js';
import { S, noeud, media, estPlaylist, entrer, peutModifier, estProprietaire } from '../etat.js';
import { ouvrirPartage } from '../partager.js';
import { champ, zoneVue } from './elements.js';
import { P } from './page.js';
import { memoriserVue } from './stockage.js';
import { fermerResultats } from './recherche.js';

const bouton = (id, icn, texte, cls = 'bouton') => `<button type="button" class="${cls}" id="${id}">${icone(icn, 18)}${texte}</button>`;

function lignePiste(id, modifiable) {
  const m = media(id);
  const retrait = modifiable
    ? `<button type="button" class="mini retirer" data-a="retirer" title="Retirer de la playlist" aria-label="Retirer de la playlist">${icone('retirer', 14)}</button>`
    : '';
  return `<li class="piste" data-id="${id}" draggable="${modifiable}"><span class="vignette">${vignette(id, m, 18)}</span>` +
    `<span class="nom">${esc(m.nom)}</span><span class="info">${m.duree ? duree(m.duree) : ''}</span>${retrait}</li>`;
}

function entete(p, modifiable) {
  const partager = estProprietaire(p) ? bouton('vue-partager', 'inviter', 'Partager') : '';
  const lecture = modifiable ? '' : '<span class="info">Lecture seule</span>';
  return `<div class="outils"><h2>${esc(p.nom)}</h2>${lecture}${partager}${bouton('vue-entrer', 'entrer', 'Entrer', 'bouton principal')}</div>`;
}

let vueAffichee = null;
export function rendreVue() {
  if (P.vue && !estPlaylist(P.vue)) { P.vue = null; memoriserVue(''); }
  zoneVue.hidden = !P.vue;
  if (P.vue !== vueAffichee) { fermerResultats(); champ.value = ''; vueAffichee = P.vue; }
  if (!P.vue) return;
  const p = noeud(P.vue), modifiable = peutModifier(p), ids = (p.pistes || []).filter((id) => media(id));
  $('#vue .ajout').hidden = !modifiable;
  $('#import').hidden = !S.imports[P.vue]?.en_cours;
  $('#liste').innerHTML = entete(p, modifiable) +
    (ids.length ? `<ul class="pistes">${ids.map((id) => lignePiste(id, modifiable)).join('')}</ul>` : '<div class="vide-zone"><p class="vide-label">Playlist vide</p></div>');
  $('#vue-entrer').onclick = () => entrer(P.vue);
  const partager = $('#vue-partager');
  if (partager) partager.onclick = () => ouvrirPartage(P.vue);
}

export function choisirVue(id) {
  P.vue = id; memoriserVue(id);
  rendreVue();
}
