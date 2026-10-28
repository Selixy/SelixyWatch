import { actionPlaylist, noeud, peutModifier } from '../etat.js';
import { zoneVue } from './elements.js';
import { P, essayer, rendre } from './page.js';
import { ajouterLien } from './liens.js';
import { avecFichiers, avecTexte, lienDepose } from './depot.js';
import { effacerIndicateurs } from './indicateurs.js';
import { envoyer } from './envoi.js';

const modifiable = () => peutModifier(noeud(P.vue));

function placePiste(e) {
  const li = e.target.closest('.piste');
  if (!li) return { avant: null, zone: 'fin', ligne: zoneVue.querySelector('.piste:last-child') };
  const r = li.getBoundingClientRect();
  if (e.clientY - r.top < r.height / 2) return { avant: li.dataset.id, zone: 'avant', ligne: li };
  const suivant = [...zoneVue.querySelectorAll('.piste')].filter((x) => x.dataset.id !== P.piste);
  const s = suivant[suivant.indexOf(li) + 1];
  return { avant: s ? s.dataset.id : null, zone: 'apres', ligne: li };
}

export function brancherGlisserPistes() {
  zoneVue.addEventListener('dragstart', (e) => {
    const li = e.target.closest?.('.piste');
    if (!li) return e.preventDefault();
    P.piste = li.dataset.id;
    e.dataTransfer.effectAllowed = 'copyMove';
    e.dataTransfer.setData('text/plain', P.piste);
    requestAnimationFrame(() => li.classList.add('glisse'));
  });
  zoneVue.addEventListener('dragover', (e) => {
    if (P.piste) {
      const d = placePiste(e);
      e.preventDefault(); e.dataTransfer.dropEffect = 'move';
      effacerIndicateurs();
      if (d.ligne && d.avant !== P.piste) d.ligne.classList.add(d.zone === 'avant' ? 'drop-avant' : 'drop-apres');
    } else if ((avecFichiers(e) || avecTexte(e)) && modifiable()) {
      e.preventDefault(); e.dataTransfer.dropEffect = 'copy';
      effacerIndicateurs(); zoneVue.classList.add('drop-fond');
    }
  });
  zoneVue.addEventListener('dragleave', (e) => { if (!zoneVue.contains(e.relatedTarget)) effacerIndicateurs(); });
  zoneVue.addEventListener('drop', async (e) => {
    e.preventDefault();
    const d = P.piste ? placePiste(e) : null, lien = !P.piste && !avecFichiers(e) ? lienDepose(e) : null;
    effacerIndicateurs();
    if (P.piste) {
      const m = P.piste; P.piste = null;
      if (d.avant !== m) await essayer(() => actionPlaylist(P.vue, 'deplacer', { media: m, avant: d.avant }));
      rendre();
    } else if (avecFichiers(e) && modifiable()) envoyer([...e.dataTransfer.files], P.vue);
    else if (lien && modifiable()) ajouterLien(lien, P.vue);
  });
  zoneVue.addEventListener('dragend', () => { P.piste = null; effacerIndicateurs(); if (P.enAttente) rendre(); });
}
