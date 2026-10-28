const SORTIE_MS = 300;

export function poserVoile(zone, source) {
  const voile = Object.assign(document.createElement('div'), { className: 'preparation' });
  voile.setAttribute('aria-hidden', 'true');
  voile.innerHTML = `<img src="${source}" alt="">`;
  zone.append(voile);
  requestAnimationFrame(() => voile.classList.add('visible'));
  return voile;
}

export function retirerVoile(voile) {
  voile.classList.remove('visible');
  setTimeout(() => voile.remove(), SORTIE_MS);
}
