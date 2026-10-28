import { construireMarque } from './logo.js';
import { ROUGE_COUPURE } from './couleurs.js';

const TAILLE = 64;

export const encre = () => (matchMedia('(prefers-color-scheme: dark)').matches ? '#f3f4f6' : '#1d1d1b');

export async function rendre(etat) {
  const svg = construireMarque({ encre: encre(), prefixe: 'fv', etat, taille: TAILLE, couleurLame: ROUGE_COUPURE });
  const image = new Image();
  image.src = `data:image/svg+xml;charset=utf-8,${encodeURIComponent(svg)}`;
  await image.decode();
  const toile = Object.assign(document.createElement('canvas'), { width: TAILLE, height: TAILLE });
  toile.getContext('2d').drawImage(image, 0, 0, TAILLE, TAILLE);
  return toile.toDataURL('image/png');
}
