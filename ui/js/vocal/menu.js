import { vocal, estMoi } from './etat.js';
import { esc } from '../ui.js';
import { basculerMicro, basculerCamera } from './medias.js';
import { reglerVolumePair, basculerMutePair } from './volume.js';
import { htmlMenuSoi, htmlMenuPair } from './menu-html.js';

export function fermerMenuProfil() {
  if (vocal.menu) {
    vocal.menu.menu?.remove();
    vocal.menu.targetEl?.classList.remove('menu-ouvert');
    document.getElementById('presents')?.classList.remove('menu-ouvert');
  }
  vocal.menu = null;
}

function surVolume(e, id, menu) {
  const range = e.target.closest('.menu-profil-range');
  if (!range) return;
  const vol = parseFloat(range.value);
  reglerVolumePair(id, vol);
  const valEl = menu.querySelector('.vol-val');
  if (valEl) valEl.textContent = `${Math.round(vol * 100)}%`;
  const muteBtn = menu.querySelector('[data-act="mute"]');
  if (muteBtn) {
    const muet = vocal.mutesLocaux.has(id) || vol === 0;
    muteBtn.classList.toggle('danger', muet);
    muteBtn.classList.toggle('actif', muet);
    muteBtn.querySelector('span').textContent = muet ? 'Rétablir le son' : 'Muter ce participant';
  }
}

const ACTIONS = {
  micro: basculerMicro,
  camera: basculerCamera,
  mute: basculerMutePair
};

async function surClic(e, id, targetEl) {
  e.stopPropagation();
  const btn = e.target.closest('[data-act]');
  if (!btn) return;
  await ACTIONS[btn.dataset.act]?.(id);
  ouvrirMenuProfil(id, targetEl);
}

export function ouvrirMenuProfil(id, targetEl) {
  if (vocal.menu?.id === id) {
    fermerMenuProfil();
    return;
  }
  fermerMenuProfil();

  const soi = estMoi(id);
  const nom = targetEl.getAttribute('title')?.replace(' (vous)', '') || 'Participant';
  const menu = document.createElement('div');
  menu.className = 'menu-profil';
  menu.setAttribute('role', 'menu');
  menu.innerHTML = `<div class="menu-profil-tete">${esc(nom)} ${soi ? '(Vous)' : ''}</div>` + (soi ? htmlMenuSoi() : htmlMenuPair(id, nom));
  targetEl.appendChild(menu);
  targetEl.classList.add('menu-ouvert');
  document.getElementById('presents')?.classList.add('menu-ouvert');
  vocal.menu = { id, menu, targetEl };

  menu.addEventListener('mousedown', (e) => e.stopPropagation());
  menu.addEventListener('pointerdown', (e) => e.stopPropagation());
  menu.addEventListener('input', (e) => surVolume(e, id, menu));
  menu.addEventListener('click', (e) => surClic(e, id, targetEl));
}
