import { entrer, noeud, actionArbre, peutRenommer, parentDeCreation } from '../etat.js';
import { ouvrirPartage } from '../partager.js';
import { conteneur } from './elements.js';
import { P, essayer, rendre } from './page.js';
import { ouverts, sauverOuverts, memoriserVue } from './stockage.js';
import { supprimer, quitterPartage } from './actions-suppression.js';

export function commencerRenommage(id) {
  P.edition = id;
  P.enAttente = false;
  const n = noeud(id);
  const el = conteneur.querySelector(`.ligne[data-id="${id}"] .nom`);
  if (!peutRenommer(n) || !el) { P.edition = null; return; }
  const champ = document.createElement('input');
  champ.className = 'nom-edition'; champ.value = n.nom; champ.maxLength = n.type === 'dossier' ? 60 : 120; champ.setAttribute('aria-label', 'Nom');
  el.replaceWith(champ);
  champ.focus(); champ.select();
  let fini = false;
  const terminer = async (valider) => {
    if (fini) return;
    fini = true; P.edition = null;
    const nom = champ.value.trim();
    if (valider && nom && nom !== n.nom) await essayer(() => actionArbre('renommer', { id, nom }));
    rendre();
  };
  champ.onkeydown = (e) => { e.stopPropagation(); if (e.key === 'Enter') terminer(true); else if (e.key === 'Escape') terminer(false); };
  champ.onblur = () => terminer(true);
}

export async function nouveau(type) {
  const parent = parentDeCreation(P.selection, noeud);
  if (parent !== 'racine') { ouverts.add(parent); sauverOuverts(); }
  const r = await essayer(() => actionArbre('creer', { parent, nom: type === 'dossier' ? 'Nouveau dossier' : 'Nouvelle playlist', type }));
  if (!r) return;
  P.aRenommer = r.id; P.selection = r.id;
  if (type === 'playlist') { P.vue = r.id; memoriserVue(r.id); }
  rendre();
}

const ACTIONS = {
  basculer: (id) => { if (ouverts.has(id)) ouverts.delete(id); else ouverts.add(id); sauverOuverts(); rendre(); },
  entrer: (id) => entrer(id),
  renommer: (id) => commencerRenommage(id),
  supprimer: (id) => supprimer(id),
  quitter: (id) => quitterPartage(id),
  partager: (id) => ouvrirPartage(id),
};

export function agirSur(action, id) {
  if (noeud(id) && Object.hasOwn(ACTIONS, action)) ACTIONS[action](id);
}
