export function activerDebug(ecran) {
  const boite = document.createElement('pre');
  boite.style.cssText = 'position:fixed;left:6px;top:6px;z-index:9999;margin:0;padding:6px 8px;max-width:92vw;font:11px/1.35 ui-monospace,monospace;' +
    'color:#9f9;background:rgba(0,0,0,.78);border-radius:8px;pointer-events:none;white-space:pre-wrap';
  document.body.append(boite);
  const t0 = performance.now(), lignes = [];
  const note = (x) => { lignes.push(`${String(Math.round(performance.now() - t0)).padStart(6)} ${x}`); if (lignes.length > 16) lignes.shift(); boite.textContent = lignes.join('\n'); };
  for (const t of ['pointerdown', 'pointerup', 'pointercancel', 'click', 'dblclick', 'touchstart', 'touchend']) {
    addEventListener(t, (e) => note(`${t} ${e.pointerType || ''} ${e.target.id || e.target.className || e.target.tagName}`), true);
  }
  new MutationObserver(() => note(`commandes ${ecran.classList.contains('repos') ? 'MASQUEES' : 'visibles'}`)).observe(ecran, { attributes: true, attributeFilter: ['class'] });
  note(`diagnostic actif (${navigator.userAgent.match(/(iPhone|iPad|Android)[^;)]*/)?.[0] || 'ordinateur'})`);
}
