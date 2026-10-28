import { $ } from '../ui.js';
import { elements } from './contexte.js';
import { plein } from './salle-etat.js';
import { lireLocal, ecrireLocal } from './stockage.js';

export function initDisposition() {
  const { salle } = elements;
  const mobile = matchMedia('(max-width: 899px)');
  let devant = lireLocal('mu-devant', 'file') === 'chat' ? 'chat' : 'file';
  const poser = () => {
    salle.dataset.devant = devant;
    const pl = plein();
    $('.file').inert = pl || (mobile.matches && devant !== 'file');
    $('#chat').inert = pl ? !salle.classList.contains('chat-ouvert') : (mobile.matches && devant !== 'chat');
  };
  salle.addEventListener('etat', poser);
  const choisir = (v) => { devant = v; ecrireLocal('mu-devant', v); poser(); };
  $('#vers-chat').onclick = () => choisir('chat');
  $('#vers-file').onclick = () => choisir('file');
  mobile.addEventListener('change', poser);
  poser();
}
