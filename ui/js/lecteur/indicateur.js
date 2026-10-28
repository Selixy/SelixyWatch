import { $ } from '../ui.js';

let minuteur = 0;

export function indiquer(contenu) {
  const i = $('#indic');
  i.innerHTML = contenu;
  i.classList.remove('vu'); void i.offsetWidth; i.classList.add('vu');
  clearTimeout(minuteur);
  minuteur = setTimeout(() => i.classList.remove('vu'), 700);
}
