import test from 'node:test';
import assert from 'node:assert/strict';
import { construireMot } from '../../ui/js/marque/mot.js';
import { MOT } from '../../ui/js/marque/formes-texte.js';

test('le mot a un chemin par lettre', () => {
  assert.equal(MOT.chemins.length, 'elixyWatch'.length);
  assert.equal(construireMot().match(/<path /g).length, 10);
});

test('la largeur suit la hauteur sans déformer', () => {
  const svg = construireMot({ taille: 34 });
  const largeur = Number(svg.match(/ width="([\d.]+)"/)[1]);
  assert.ok(Math.abs(largeur - (34 * MOT.largeur) / 64) < 0.06);
  const hauteur = Number(svg.match(/ height="([\d.]+)"/)[1]);
  assert.ok(Math.abs(hauteur - (34 * MOT.hauteur) / 64) < 0.06);
});

test("le mot n'a pas de police et se colore par la couleur du texte", () => {
  const svg = construireMot();
  assert.ok(svg.includes('fill="currentColor"'));
  assert.ok(!svg.includes('<text'));
});
