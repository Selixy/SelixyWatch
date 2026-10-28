const APPARITION = {
  duree: 0.3,
  temps: [0, 0.25, 0.3],
  largeur: [0, 1, 1],
  epaisseur: [1, 1, 1],
  courbes: [[0.05, 0.9, 0.15, 1], [0, 0, 1, 1]],
};

const DISPARITION = {
  duree: 0.3,
  temps: [0, 0.3],
  largeur: [1, 0],
  epaisseur: [1, 1],
  courbes: [[0.6, 0, 0.2, 1]],
};

export const SEQUENCES = { apparition: APPARITION, disparition: DISPARITION };

export function courbeBezier(x1, y1, x2, y2) {
  const coord = (a, b, u) => 3 * a * u * (1 - u) ** 2 + 3 * b * u * u * (1 - u) + u ** 3;
  return (x) => {
    let bas = 0;
    let haut = 1;
    for (let i = 0; i < 28; i++) {
      const milieu = (bas + haut) / 2;
      if (coord(x1, x2, milieu) < x) bas = milieu; else haut = milieu;
    }
    return coord(y1, y2, (bas + haut) / 2);
  };
}

function interpoler(valeurs, sequence, t) {
  const { temps, courbes } = sequence;
  if (t <= temps[0]) return valeurs[0];
  if (t >= temps[temps.length - 1]) return valeurs[valeurs.length - 1];
  const k = temps.findIndex((instant, i) => t >= instant && t < temps[i + 1]);
  const avancement = (t - temps[k]) / (temps[k + 1] - temps[k]);
  const progres = courbeBezier(...courbes[k])(avancement);
  return valeurs[k] + (valeurs[k + 1] - valeurs[k]) * progres;
}

export function etatLame(sequence, t) {
  return { largeur: interpoler(sequence.largeur, sequence, t), epaisseur: interpoler(sequence.epaisseur, sequence, t) };
}

export const ETAT_ABSENTE = { largeur: 0, epaisseur: 1 };
export const ETAT_PRESENTE = { largeur: 1, epaisseur: 1 };
