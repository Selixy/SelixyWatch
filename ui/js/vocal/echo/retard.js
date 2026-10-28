export function creerRetard(capacite) {
  const tampon = new Float32Array(capacite);
  let tete = 0;
  return {
    ecrire(x) {
      tete = (tete + 1) % capacite;
      tampon[tete] = x;
    },
    lire(delai) {
      return tampon[(tete - delai + capacite) % capacite];
    }
  };
}
