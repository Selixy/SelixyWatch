import { actionArbre, noeud, deplacementPermis } from '../etat.js';
import { conteneur } from './elements.js';
import { P, essayer, rendre } from './page.js';
import { ouverts, sauverOuverts } from './stockage.js';
import { ajouterLien } from './liens.js';
import { avecFichiers, avecTexte, lienDepose } from './depot.js';
import { effacerIndicateurs, indiquer } from './indicateurs.js';
import { estDescendant, destination, valide, playlistVisee } from './glisser-arbre-decision.js';
import { ajouterA } from './actions-pistes.js';
import { envoyer } from './envoi.js';

async function deposerNoeud(d) {
  const id = P.glisse; P.glisse = null;
  if (!estDescendant(d.vers, id) && d.vers !== id && d.avant !== id && deplacementPermis(noeud(id), d.vers, noeud)) {
    if (d.vers !== 'racine') { ouverts.add(d.vers); sauverOuverts(); }
    await essayer(() => actionArbre('deplacer', { id, vers: d.vers, avant: d.avant }));
  }
  rendre();
}

async function deposerPiste(p) {
  const m = P.piste; P.piste = null;
  if (p && p !== P.vue) await ajouterA(p, m);
  rendre();
}

export function brancherGlisserArbre() {
  conteneur.addEventListener('dragstart', (e) => {
    const l = e.target.closest?.('.ligne');
    if (!l) return e.preventDefault();
    P.glisse = l.dataset.id;
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/plain', P.glisse);
    requestAnimationFrame(() => l.classList.add('glisse'));
  });
  conteneur.addEventListener('dragover', (e) => {
    if (P.glisse) {
      const d = destination(e);
      if (valide(d)) { e.preventDefault(); e.dataTransfer.dropEffect = 'move'; indiquer(d); } else effacerIndicateurs();
    } else if (P.piste || avecFichiers(e) || avecTexte(e)) {
      const p = playlistVisee(e);
      if (p && !(P.piste && p === P.vue)) { e.preventDefault(); e.dataTransfer.dropEffect = 'copy'; indiquer({ zone: 'dans', ligne: e.target.closest('.ligne') }); } else effacerIndicateurs();
    }
  });
  conteneur.addEventListener('dragleave', (e) => { if (!conteneur.contains(e.relatedTarget)) effacerIndicateurs(); });
  conteneur.addEventListener('drop', async (e) => {
    e.preventDefault();
    const d = P.glisse ? destination(e) : null, p = playlistVisee(e), lien = !P.glisse && !P.piste && !avecFichiers(e) ? lienDepose(e) : null;
    effacerIndicateurs();
    if (P.glisse) await deposerNoeud(d);
    else if (P.piste) await deposerPiste(p);
    else if (p && avecFichiers(e)) envoyer([...e.dataTransfer.files], p);
    else if (p && lien) ajouterLien(lien, p);
  });
  conteneur.addEventListener('dragend', () => { P.glisse = null; effacerIndicateurs(); if (P.enAttente) rendre(); });
}
