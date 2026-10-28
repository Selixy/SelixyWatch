import { creerFiltre } from './filtre.js';
import { creerRetard } from './retard.js';
import { creerEstimateur } from './estimateur.js';

const LONGUEUR_FILTRE = 512;
const PAS_ADAPTATION = 0.05;
const SEUIL_ECHO = 1e-6;
const RAPPORT_VOIX = 0.3;
const GAIN_RESIDUEL = 0.15;
const ECART_RETARD = 100;

export function creerAnnuleur(taux) {
  const filtre = creerFiltre(LONGUEUR_FILTRE, PAS_ADAPTATION);
  const retard = creerRetard(Math.ceil(taux));
  const estimateur = creerEstimateur(taux);
  const lissage = 1 / (taux * 0.02);
  const fermeture = 1 / (taux * 0.01);
  const ouverture = 1 / (taux * 0.003);
  let delai = 0;
  let puissanceEcho = 0;
  let puissanceErreur = 0;
  let gain = 1;
  return {
    traiter(mic, ref) {
      retard.ecrire(ref);
      filtre.pousser(retard.lire(delai));
      const echo = filtre.estimer();
      const erreur = mic - echo;
      filtre.adapter(erreur);
      puissanceEcho += (echo * echo - puissanceEcho) * lissage;
      puissanceErreur += (erreur * erreur - puissanceErreur) * lissage;
      const seulEcho = puissanceEcho > SEUIL_ECHO && puissanceErreur < RAPPORT_VOIX * puissanceEcho;
      const cible = seulEcho ? GAIN_RESIDUEL : 1;
      gain += (cible - gain) * (cible < gain ? fermeture : ouverture);
      const mesure = estimateur.observer(ref, mic);
      const voulu = Math.max(0, mesure - LONGUEUR_FILTRE / 2);
      if (mesure >= 0 && Math.abs(voulu - delai) > ECART_RETARD) delai = voulu;
      return erreur * gain;
    }
  };
}
