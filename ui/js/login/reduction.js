const COTE = 128;
const QUALITE = 0.85;

export async function reduire(fichier) {
  const bmp = await createImageBitmap(fichier);
  const c = Math.min(bmp.width, bmp.height);
  const toile = document.createElement('canvas');
  toile.width = toile.height = COTE;
  toile.getContext('2d').drawImage(bmp, (bmp.width - c) / 2, (bmp.height - c) / 2, c, c, 0, 0, COTE, COTE);
  bmp.close();
  const blob = (type) => new Promise((ok) => toile.toBlob(ok, type, QUALITE));
  const b = await blob('image/webp');
  return b?.type === 'image/webp' ? b : blob('image/jpeg');
}
