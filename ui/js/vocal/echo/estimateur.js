const POINTS = 512;
const RETARD_MAX = 250;
const INTERVALLE = 125;
const CONFIANCE_MIN = 0.15;
const CADENCE = 500;

function ordonner(anneau, ecrits) {
  const sortie = new Float32Array(POINTS);
  let moyenne = 0;
  for (let i = 0; i < POINTS; i++) {
    sortie[i] = anneau[(ecrits + i) % POINTS];
    moyenne += sortie[i];
  }
  moyenne /= POINTS;
  for (let i = 0; i < POINTS; i++) sortie[i] -= moyenne;
  return sortie;
}

function normeCarree(serie) {
  let somme = 0;
  for (const v of serie) somme += v * v;
  return somme;
}

function meilleurRetard(mic, ref) {
  const norme = Math.sqrt(normeCarree(mic) * normeCarree(ref));
  if (norme < 1e-9) return -1;
  let meilleur = -1;
  let score = CONFIANCE_MIN;
  for (let retard = 0; retard <= RETARD_MAX; retard++) {
    let somme = 0;
    for (let i = retard; i < POINTS; i++) somme += mic[i] * ref[i - retard];
    if (somme / norme > score) {
      score = somme / norme;
      meilleur = retard;
    }
  }
  return meilleur;
}

export function creerEstimateur(taux) {
  const pas = Math.round(taux / CADENCE);
  const enveloppeRef = new Float32Array(POINTS);
  const enveloppeMic = new Float32Array(POINTS);
  let sommeRef = 0;
  let sommeMic = 0;
  let compte = 0;
  let ecrits = 0;
  return {
    observer(ref, mic) {
      sommeRef += Math.abs(ref);
      sommeMic += Math.abs(mic);
      if (++compte < pas) return -1;
      enveloppeRef[ecrits % POINTS] = sommeRef / pas;
      enveloppeMic[ecrits % POINTS] = sommeMic / pas;
      sommeRef = sommeMic = compte = 0;
      ecrits++;
      if (ecrits < POINTS || ecrits % INTERVALLE !== 0) return -1;
      const retard = meilleurRetard(ordonner(enveloppeMic, ecrits), ordonner(enveloppeRef, ecrits));
      return retard < 0 ? -1 : retard * pas;
    }
  };
}
