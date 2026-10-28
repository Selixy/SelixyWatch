export const segmentApres = (segments, t) => segments.findIndex((s) => s.fin > t + 0.05);

export function tamponComplet(tampon, segments) {
  const dernier = segments[segments.length - 1];
  const fin = tampon.buffered.length ? tampon.buffered.end(tampon.buffered.length - 1) : 0;
  return !!dernier && fin >= dernier.fin - 0.5;
}
