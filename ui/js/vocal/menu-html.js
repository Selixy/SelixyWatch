import { vocal, monEtat, etatDe } from './etat.js';
import { esc } from '../ui.js';

export function htmlMenuSoi() {
  return `
      <button type="button" class="menu-profil-bouton ${monEtat.micro ? 'actif' : ''}" data-act="micro">
        <span>${monEtat.micro ? 'Couper le micro' : 'Activer le micro'}</span>
      </button>
      <button type="button" class="menu-profil-bouton ${monEtat.camera ? 'actif' : ''}" data-act="camera">
        <span>${monEtat.camera ? 'Couper la caméra' : 'Activer la caméra'}</span>
      </button>
    `;
}

export function htmlMenuPair(id, nom) {
  const etat = etatDe(id);
  const muet = vocal.mutesLocaux.has(id);
  const vol = muet ? 0 : (vocal.volumesLocaux.get(id) ?? 1);
  return `
      <div class="menu-profil-statut">
        <span>Micro: <b>${etat.micro ? 'Actif' : 'Coupé'}</b></span>
        <span>Caméra: <b>${etat.camera ? 'Active' : 'Coupée'}</b></span>
      </div>
      <div class="menu-profil-volume">
        <div class="menu-profil-volume-tete">
          <span>Volume</span>
          <span class="vol-val">${Math.round(vol * 100)}%</span>
        </div>
        <input type="range" class="menu-profil-range" min="0" max="1" step="0.01" value="${vol}" aria-label="Volume de ${esc(nom)}">
      </div>
      <button type="button" class="menu-profil-bouton ${muet ? 'danger actif' : ''}" data-act="mute">
        <span>${muet ? 'Rétablir le son' : 'Muter ce participant'}</span>
      </button>
    `;
}
