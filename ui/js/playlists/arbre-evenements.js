import { estDossier, estPlaylist } from '../etat.js';
import { conteneur } from './elements.js';
import { P } from './page.js';
import { agirSur, commencerRenommage } from './actions-arbre.js';
import { supprimer } from './actions-suppression.js';
import { choisirVue } from './vue-pistes.js';

export function brancherArbre() {
  conteneur.addEventListener('click', (e) => {
    const l = e.target.closest('.ligne');
    if (!l || e.target.closest('.nom-edition')) return;
    const b = e.target.closest('[data-a]');
    if (b) return agirSur(b.dataset.a, l.dataset.id);
    P.selection = l.dataset.id;
    conteneur.querySelectorAll('.ligne.select, .ligne.vue-courante').forEach((x) => x.classList.remove('select', 'vue-courante'));
    l.classList.add('select');
    if (estPlaylist(P.selection)) { l.classList.add('vue-courante'); choisirVue(P.selection); }
  });
  conteneur.addEventListener('dblclick', (e) => {
    const l = e.target.closest('.ligne');
    if (!l || e.target.closest('.nom-edition, [data-a]')) return;
    agirSur(estDossier(l.dataset.id) ? 'basculer' : 'entrer', l.dataset.id);
  });
  conteneur.addEventListener('keydown', (e) => {
    const l = e.target.closest('.ligne');
    if (!l || e.target.matches('input')) return;
    const id = l.dataset.id;
    if (e.key === 'F2') { e.preventDefault(); commencerRenommage(id); }
    else if (e.key === 'Delete') { e.preventDefault(); supprimer(id); }
    else if (e.key === 'Enter') { e.preventDefault(); agirSur(estDossier(id) ? 'basculer' : 'entrer', id); }
    else if (e.key === ' ') {
      e.preventDefault();
      if (estDossier(id)) agirSur('basculer', id); else l.click();
    }
  });
}
