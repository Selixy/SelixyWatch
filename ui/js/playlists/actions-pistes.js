import { S, noeud, media, actionPlaylist } from '../etat.js';
import { zoneVue } from './elements.js';
import { P, essayer, message } from './page.js';

export async function ajouterA(playlist, mediaId) {
  if (noeud(playlist)?.pistes?.includes(mediaId)) return message('Déjà dans cette playlist.');
  await essayer(() => actionPlaylist(playlist, 'ajouter', { media: mediaId }));
}

async function retirer(mediaId) {
  const m = media(mediaId);
  const ailleurs = S.noeuds.some((n) => n.type === 'playlist' && n.id !== P.vue && n.pistes?.includes(mediaId));
  if (!ailleurs && !confirm(`Retirer « ${m?.nom ?? ''} » ? Il n'est dans aucune autre playlist et sera supprimé.`)) return;
  await essayer(() => actionPlaylist(P.vue, 'retirer', { media: mediaId }));
}

export function brancherRetrait() {
  zoneVue.addEventListener('click', (e) => {
    const b = e.target.closest('[data-a="retirer"]');
    if (b) retirer(b.closest('.piste').dataset.id);
  });
}
