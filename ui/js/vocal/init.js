import { moi } from '../compte.js';
import { vocal } from './etat.js';
import { ajusterTaillesPresents } from './taille.js';
import { fermerMenuProfil } from './menu.js';
import { ecouterSignaux } from './ecoute.js';
import { initSonGeneral } from './general.js';

export async function initVocal() {
  vocal.moi = await moi();

  document.addEventListener('click', (e) => {
    if (vocal.menu && !e.target.closest('.menu-profil') && !e.target.closest('.present')) {
      fermerMenuProfil();
    }
  });
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') fermerMenuProfil();
  });
  window.addEventListener('resize', ajusterTaillesPresents);

  ecouterSignaux();
  initSonGeneral();
}
