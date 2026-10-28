const MIN_L = 320, MIN_H = 180;

export async function versJpeg(source, l, h) {
  const toile = document.createElement('canvas');
  toile.width = MIN_L; toile.height = MIN_H;
  const c = Math.max(MIN_L / l, MIN_H / h);
  toile.getContext('2d').drawImage(source, (MIN_L - l * c) / 2, (MIN_H - h * c) / 2, l * c, h * c);
  return new Promise((ok) => toile.toBlob(ok, 'image/jpeg', 0.75));
}
