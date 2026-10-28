import test from 'node:test';
import assert from 'node:assert/strict';
import { lireJeton, garder, enAttente, effacer, CLE } from '../../ui/js/invitation/jeton.js';

const stockageFactice = () => {
  const m = new Map();
  return { setItem: (k, v) => m.set(k, v), getItem: (k) => m.get(k) ?? null, removeItem: (k) => m.delete(k) };
};

test('le jeton se lit dans le fragment et les fragments invalides sont refusés', () => {
  assert.equal(lireJeton('#abcDEF123_-xyz'), 'abcDEF123_-xyz');
  for (const h of ['', '#', '#court', '#a b c d e f g h', null]) assert.equal(lireJeton(h), null);
});

test('le jeton en attente se garde, se relit et s\'efface', () => {
  const s = stockageFactice();
  assert.equal(enAttente(s), null);
  garder(s, 'jeton-de-test-1');
  assert.equal(s.getItem(CLE), 'jeton-de-test-1');
  assert.equal(enAttente(s), 'jeton-de-test-1');
  effacer(s);
  assert.equal(enAttente(s), null);
});

test('un stockage indisponible ne casse rien', () => {
  const casse = { setItem() { throw new Error('x'); }, getItem() { throw new Error('x'); }, removeItem() { throw new Error('x'); } };
  garder(casse, 'jeton-de-test-1');
  assert.equal(enAttente(casse), null);
  effacer(casse);
});
