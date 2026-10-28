import test from 'node:test';
import assert from 'node:assert/strict';
import { lireBoites, lireSidx } from '../../ui/js/lecteur/flux/mp4.js';
import { construireEntete, TAILLE_SEGMENT, DUREE_SEGMENT } from './mp4-factice.js';

test('trouve les boîtes de premier niveau', () => {
  const types = lireBoites(construireEntete(3)).map((b) => b.type);
  assert.deepEqual(types, ['ftyp', 'moov', 'sidx']);
});

test('lit les segments du sidx avec leurs positions', () => {
  const octets = construireEntete(3);
  const sidx = lireBoites(octets).find((b) => b.type === 'sidx');
  const segments = lireSidx(octets, sidx);
  assert.equal(segments.length, 3);
  assert.equal(segments[0].octet, octets.length);
  assert.equal(segments[2].octet, octets.length + 2 * TAILLE_SEGMENT);
  assert.deepEqual([segments[1].debut, segments[1].fin], [DUREE_SEGMENT, 2 * DUREE_SEGMENT]);
});

test('ignore une boîte tronquée sans planter', () => {
  const octets = construireEntete(3);
  assert.equal(lireBoites(octets.subarray(0, octets.length - 5)).length, 3);
  assert.deepEqual(lireBoites(new Uint8Array(4)), []);
});
