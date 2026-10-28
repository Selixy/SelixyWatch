import { rendre } from './favicon-image.js';
import { SEQUENCES, etatLame, ETAT_ABSENTE, ETAT_PRESENTE } from './lame-rythme.js';

const PAS_IMAGE_MS = 80;

function lien() {
  let l = document.querySelector('link[data-marque]');
  if (l) return l;
  document.querySelectorAll('link[rel="icon"]').forEach((ancien) => ancien.remove());
  l = Object.assign(document.createElement('link'), { rel: 'icon', type: 'image/png', sizes: '64x64' });
  l.dataset.marque = '';
  document.head.append(l);
  return l;
}

async function poser(etat, coupe, valide) {
  try {
    const url = await rendre(etat);
    if (valide()) lien().href = url;
  } catch {
    if (valide()) Object.assign(lien(), { type: 'image/svg+xml', href: coupe ? '/visuels/favicon-coupe.svg' : '/visuels/favicon.svg' });
  }
}

export function creerFavicon() {
  let generation = 0;
  let coupeActuelle = false;
  const courante = () => { const moi = generation; return () => moi === generation; };
  const final = () => (coupeActuelle ? ETAT_PRESENTE : ETAT_ABSENTE);
  matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => poser(final(), coupeActuelle, courante()));
  return async (coupe, animer) => {
    generation += 1;
    coupeActuelle = coupe;
    const valide = courante();
    const sequence = SEQUENCES[coupe ? 'apparition' : 'disparition'];
    for (let t = 0; animer && t < sequence.duree && valide(); t += PAS_IMAGE_MS / 1000) {
      await poser(etatLame(sequence, t), coupe, valide);
      await new Promise((r) => setTimeout(r, PAS_IMAGE_MS));
    }
    await poser(final(), coupe, valide);
  };
}
