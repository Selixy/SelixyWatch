import { versJpeg } from './jpeg.js';

export async function pochetteMp3(f) {
  const o = new Uint8Array(await f.slice(0, 1 << 20).arrayBuffer());
  if (String.fromCharCode(o[0], o[1], o[2]) !== 'ID3') return null;
  const v4 = o[3] === 4, fin = Math.min(10 + ((o[6] << 21) | (o[7] << 14) | (o[8] << 7) | o[9]), o.length);
  for (let i = 10; i + 10 < fin;) {
    const id = String.fromCharCode(o[i], o[i + 1], o[i + 2], o[i + 3]);
    if (!/^[A-Z0-9]{4}$/.test(id)) return null;
    const n = v4 ? (o[i + 4] << 21) | (o[i + 5] << 14) | (o[i + 6] << 7) | o[i + 7] : o[i + 4] * 16777216 + (o[i + 5] << 16) + (o[i + 6] << 8) + o[i + 7];
    if (id === 'APIC') {
      let k = i + 10;
      const codage = o[k++];
      while (k < fin && o[k] !== 0) k++;
      k += 2;
      if (codage === 1 || codage === 2) { while (k + 1 < fin && !(o[k] === 0 && o[k + 1] === 0)) k += 2; k += 2; }
      else { while (k < fin && o[k] !== 0) k++; k++; }
      const image = await createImageBitmap(new Blob([o.slice(k, i + 10 + n)]));
      return versJpeg(image, image.width, image.height);
    }
    i += 10 + n;
  }
  return null;
}
