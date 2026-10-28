export function jouerSequence(sequence, surImage, surFin) {
  const debut = performance.now();
  let identifiant = 0;
  const pas = (maintenant) => {
    const t = (maintenant - debut) / 1000;
    if (t >= sequence.duree) { surFin(); return; }
    surImage(t);
    identifiant = requestAnimationFrame(pas);
  };
  identifiant = requestAnimationFrame(pas);
  return () => cancelAnimationFrame(identifiant);
}
