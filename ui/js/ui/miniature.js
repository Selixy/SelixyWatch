import { esc } from './dom.js';
import { icone } from './icone.js';

export const urlMiniature = (id, m) =>
  m?.source === 'youtube' ? `https://i.ytimg.com/vi/${m.yt}/mqdefault.jpg` : m?.mini ? `/medias/${id}-mini.jpg?v=${m.t}` : null;

export function vignette(id, m, taille = 20) {
  const u = urlMiniature(id, m);
  return u ? `<img src="${esc(u)}" alt="" loading="lazy">` : icone(m?.genre === 'audio' ? 'musique' : 'video', taille);
}
