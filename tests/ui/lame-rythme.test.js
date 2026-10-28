import test from 'node:test';
import assert from 'node:assert/strict';
import { SEQUENCES, etatLame, courbeBezier } from '../../ui/js/marque/lame-rythme.js';

test('la courbe linéaire rend son entrée', () => {
  const lineaire = courbeBezier(0, 0, 1, 1);
  for (const x of [0, 0.25, 0.5, 1]) assert.ok(Math.abs(lineaire(x) - x) < 0.001);
});

test("l'apparition part de rien et finit lame pleine", () => {
  const { apparition } = SEQUENCES;
  assert.deepEqual(etatLame(apparition, 0), { largeur: 0, epaisseur: 1 });
  assert.deepEqual(etatLame(apparition, apparition.duree), { largeur: 1, epaisseur: 1 });
});

test("l'épaisseur ne change jamais : le logo est trop petit pour la voir bouger", () => {
  for (const sequence of Object.values(SEQUENCES)) {
    for (let t = 0; t <= sequence.duree; t += 0.01) assert.equal(etatLame(sequence, t).epaisseur, 1);
  }
});

test('la lame se dessine sans jamais reculer', () => {
  const { apparition } = SEQUENCES;
  let precedent = -1;
  for (let t = 0; t <= apparition.duree; t += 0.01) {
    const { largeur } = etatLame(apparition, t);
    assert.ok(largeur >= precedent - 1e-9);
    precedent = largeur;
  }
});

test('la lame se retire sans jamais repartir', () => {
  const { disparition } = SEQUENCES;
  let precedent = 2;
  for (let t = 0; t <= disparition.duree; t += 0.01) {
    const { largeur } = etatLame(disparition, t);
    assert.ok(largeur <= precedent + 1e-9);
    precedent = largeur;
  }
  assert.equal(etatLame(disparition, disparition.duree).largeur, 0);
});
