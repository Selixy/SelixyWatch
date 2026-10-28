import test from 'node:test';
import assert from 'node:assert/strict';
import { creerPorte } from '../../ui/js/vocal/echo/porte.js';

const TAUX = 16000;
const bruit = (i) => 0.07 * Math.sin(i * 12.9898) * Math.cos(i * 78.233);
const voix = (i) => 0.3 * Math.sin(i * 0.2);
const energie = (serie, de, a) => serie.slice(de, a).reduce((s, v) => s + v * v, 0);

test('la porte retient un fond constant et laisse passer la voix', () => {
  const porte = creerPorte(TAUX);
  const entree = new Float32Array(10 * TAUX).map((_, i) => bruit(i) + (i > 7 * TAUX && Math.floor(i / (TAUX / 2)) % 2 === 0 ? voix(i) : 0));
  const sortie = entree.map((x) => porte.traiter(x));
  const attenuation = 10 * Math.log10(energie(entree, 4 * TAUX, 6 * TAUX) / energie(sortie, 4 * TAUX, 6 * TAUX));
  const conservee = energie(sortie, 8 * TAUX, 10 * TAUX) / energie(entree, 8 * TAUX, 10 * TAUX);
  assert.ok(energie(entree, 8 * TAUX, 10 * TAUX) > 0);
  assert.ok(attenuation > 15, `fond atténué de ${attenuation.toFixed(1)} dB`);
  assert.ok(conservee > 0.8, `voix conservée à ${conservee.toFixed(2)}`);
});

test('une voix qui parle dès le début n\'est pas prise pour du fond', () => {
  const porte = creerPorte(TAUX);
  const parole = (i) => (Math.floor(i / (TAUX / 3)) % 2 === 0 ? voix(i) * (0.6 + 0.4 * Math.sin(i * 0.002)) : 0);
  const entree = new Float32Array(8 * TAUX).map((_, i) => 0.003 * bruit(i) + parole(i));
  const sortie = entree.map((x) => porte.traiter(x));
  const conservee = energie(sortie, 0, 8 * TAUX) / energie(entree, 0, 8 * TAUX);
  assert.ok(conservee > 0.8, `voix conservée à ${conservee.toFixed(2)}`);
});
