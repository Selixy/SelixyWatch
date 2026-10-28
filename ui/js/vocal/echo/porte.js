const PLANCHER = 0.006;
const FACTEUR = 2.5;
const ATTENTE = 0.3;
const GAIN_FERME = 0.1;

export function creerPorte(taux) {
  const lissage = 1 / (taux * 0.005);
  const rapide = 1 / taux;
  const lent = 1 / (taux * 6);
  const montee = 1 / (taux * 0.005);
  const descente = 1 / (taux * 0.08);
  let puissance = 0;
  let fond = 0;
  let ouverte = false;
  let restant = 0;
  let gain = 0;
  return {
    traiter(x) {
      puissance += (x * x - puissance) * lissage;
      const niveau = Math.sqrt(puissance);
      if (niveau > Math.max(PLANCHER, fond * FACTEUR)) {
        ouverte = true;
        restant = ATTENTE * taux;
      } else if (restant > 0) {
        restant--;
      } else {
        ouverte = false;
      }
      fond = niveau < fond ? niveau : fond + (niveau - fond) * (ouverte ? lent : rapide);
      const cible = ouverte ? 1 : GAIN_FERME;
      gain += (cible - gain) * (cible > gain ? montee : descente);
      return x * gain;
    }
  };
}
