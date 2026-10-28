import { esc } from '../ui.js';

let voile = null;

function surTouche(e) { if (e.key === 'Escape') fermer(); }

export function fermer() {
  voile?.remove();
  voile = null;
  document.removeEventListener('keydown', surTouche);
}

export function ouvrirFenetre(titre, corps) {
  fermer();
  voile = document.createElement('div');
  voile.className = 'voile';
  voile.innerHTML = `<div class="carte partage" role="dialog" aria-modal="true" aria-label="${esc(titre)}"><div class="outils"><h2>${esc(titre)}</h2>` +
    `<button type="button" class="bouton" data-a="fermer">Fermer</button></div>${corps}<p class="message" role="status"></p></div>`;
  document.body.append(voile);
  document.addEventListener('keydown', surTouche);
  return voile;
}
