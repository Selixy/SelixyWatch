import { versJpeg } from './jpeg.js';
import { pochetteMp3 } from './pochette-mp3.js';

function imageVideo(f) {
  return new Promise((ok) => {
    const v = document.createElement('video'), u = URL.createObjectURL(f);
    const fin = (r) => { clearTimeout(garde); URL.revokeObjectURL(u); v.removeAttribute('src'); ok(r); };
    const garde = setTimeout(() => fin(null), 8000);
    v.muted = true; v.preload = 'auto'; v.playsInline = true;
    v.onerror = () => fin(null);
    v.onloadedmetadata = () => { v.currentTime = Math.min(1, (v.duration || 2) * 0.1); };
    v.onseeked = async () => { try { fin(v.videoWidth ? await versJpeg(v, v.videoWidth, v.videoHeight) : null); } catch { fin(null); } };
    v.src = u;
  });
}

async function miniatureFichier(f) {
  try {
    if (/\.mp3$/i.test(f.name)) return await pochetteMp3(f);
    if (f.type.startsWith('video/') || /\.(mp4|m4v|mov|webm)$/i.test(f.name)) return await imageVideo(f);
  } catch { return null; }
  return null;
}

export async function envoyerMiniature(f, reponse) {
  let id; try { id = JSON.parse(reponse).id; } catch { return; }
  const image = id && await miniatureFichier(f);
  if (image && image.size <= 200 * 1024) await fetch(`/api/medias/${id}/miniature`, { method: 'POST', credentials: 'same-origin', headers: { 'Content-Type': 'image/jpeg' }, body: image }).catch(() => {});
}
