export function attendreLecture(yt) {
  if (yt.enCours) return yt.enCours;
  yt.lecteur.playVideo();
  const t0 = Date.now();
  yt.enCours = new Promise((ok, ko) => {
    const iv = setInterval(() => {
      const s = yt.etat();
      if (s === 1) { clearInterval(iv); ok(); }
      else if (Date.now() - t0 > 4000) { clearInterval(iv); s === 3 ? ok() : ko(new Error('bloqué')); }
    }, 150);
  }).finally(() => { yt.enCours = null; });
  return yt.enCours;
}

export function arreter(lecteur) {
  try { lecteur.stopVideo(); } catch { return false; }
  return true;
}
