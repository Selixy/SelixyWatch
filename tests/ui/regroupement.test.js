import test from 'node:test';
import assert from 'node:assert/strict';
import { regrouper } from '../../ui/js/etat/regroupement.js';

test('des demandes rapprochées ne donnent qu\'une lecture', async () => {
  const taches = [];
  let lectures = 0;
  const demander = regrouper(async () => { lectures += 1; }, 100, (f) => taches.push(f));
  demander(); demander(); demander();
  assert.equal(taches.length, 1);
  await taches.shift()();
  assert.equal(lectures, 1);
});

test('une demande pendant une lecture en provoque une seconde', async () => {
  const taches = [];
  let lectures = 0;
  const demander = regrouper(async () => { lectures += 1; if (lectures === 1) demander(); }, 100, (f) => taches.push(f));
  demander();
  await taches.shift()();
  assert.equal(taches.length, 1);
  await taches.shift()();
  assert.equal(lectures, 2);
});
