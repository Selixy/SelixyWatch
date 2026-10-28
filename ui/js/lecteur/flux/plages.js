export function finTamponnee(tampon, t) {
  for (let i = 0; i < tampon.buffered.length; i++) {
    if (tampon.buffered.start(i) - 0.1 <= t && t <= tampon.buffered.end(i)) return tampon.buffered.end(i);
  }
  return null;
}

export const debutTamponne = (tampon) => (tampon.buffered.length ? tampon.buffered.start(0) : null);
