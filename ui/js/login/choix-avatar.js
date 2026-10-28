import { $ } from '../ui.js';
import { saisie } from './saisie.js';
import { message, apercu } from './affichage.js';
import { reduire } from './reduction.js';

async function choisir(e) {
  const f = e.target.files[0];
  e.target.value = '';
  if (!f) return;
  try { saisie.image = await reduire(f); saisie.retirer = false; message(''); apercu(); }
  catch { message('Image illisible.'); }
}

export function brancherChoixAvatar() {
  $('#choisir-avatar').onclick = () => $('#fichier-avatar').click();
  $('#fichier-avatar').onchange = choisir;
  $('#retirer-avatar').onclick = () => { saisie.image = null; saisie.retirer = true; apercu(); };
  $('#pseudo').oninput = apercu;
}
