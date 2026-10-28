import test from 'node:test';
import assert from 'node:assert/strict';
import { meilleureTaille } from '../../ui/js/vocal/taille.js';

test('une seule caméra prend la plus petite dimension', () => {
  assert.equal(meilleureTaille(1, 500, 200, 16), 200);
});

test('plusieurs caméras tiennent dans la zone, en ligne ou sur plusieurs lignes', () => {
  for (const [n, l, h] of [[2, 500, 200], [3, 500, 200], [4, 300, 300], [6, 400, 260], [9, 320, 600]]) {
    const t = meilleureTaille(n, l, h, 16);
    const colonnes = Math.max(1, Math.floor((l + 16) / (t + 16)));
    const lignes = Math.ceil(n / colonnes);
    assert.ok(colonnes * t + (colonnes - 1) * 16 <= l + 0.001, `largeur ${n}`);
    assert.ok(lignes * t + (lignes - 1) * 16 <= h + 0.001, `hauteur ${n}`);
  }
});

test('plus il y a de caméras, plus elles rétrécissent', () => {
  assert.ok(meilleureTaille(4, 500, 200, 16) < meilleureTaille(2, 500, 200, 16));
});
