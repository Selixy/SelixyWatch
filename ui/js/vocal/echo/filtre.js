const REGULARISATION = 1e-5;

export function creerFiltre(longueur, pas) {
  const poids = new Float64Array(longueur);
  const histoire = new Float32Array(longueur * 2);
  let tete = 0;
  let energie = 0;
  return {
    pousser(x) {
      tete = (tete + longueur - 1) % longueur;
      const ancien = histoire[tete];
      energie = Math.max(0, energie + x * x - ancien * ancien);
      histoire[tete] = x;
      histoire[tete + longueur] = x;
    },
    estimer() {
      let somme = 0;
      for (let k = 0; k < longueur; k++) somme += poids[k] * histoire[tete + k];
      return somme;
    },
    adapter(erreur) {
      const gain = (pas * erreur) / (energie + REGULARISATION * longueur);
      for (let k = 0; k < longueur; k++) poids[k] += gain * histoire[tete + k];
    }
  };
}
