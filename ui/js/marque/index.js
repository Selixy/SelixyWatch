import { monterEntete } from './entete.js';
import { monterMot } from './mot.js';
import { creerFavicon } from './favicon.js';
import { ROUGE_COUPURE } from './couleurs.js';

const OPTIONS_ENTETE = { echelleS: 0.9, opaciteTele: 0.65, couleurLame: ROUGE_COUPURE };
const tailleMarque = () => parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--marque-taille')) || 30;
const estPagePrincipale = () => window.top === window;

export function initMarque(bouton, lien) {
  const taille = tailleMarque();
  const entete = monterEntete(bouton, taille, OPTIONS_ENTETE);
  monterMot(lien, taille);
  const favicon = estPagePrincipale() ? creerFavicon() : () => {};
  let coupeAvant = null;
  return {
    definirCoupe(coupe) {
      if (coupe === coupeAvant) return;
      const animer = coupeAvant !== null;
      coupeAvant = coupe;
      entete(coupe, animer);
      favicon(coupe, animer);
    },
  };
}
