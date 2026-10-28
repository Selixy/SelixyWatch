import test from 'node:test';
import assert from 'node:assert/strict';
import { calculerAudio } from '../../ui/js/vocal/volume-calcul.js';

const base = { individuel: 1, muetIndividuel: false, maitre: 0.8, muetMaitre: false };

test('le volume du participant est son réglage multiplié par le volume général', () => {
  assert.equal(calculerAudio({ ...base, individuel: 0.5 }).volume, 0.4);
  assert.equal(calculerAudio({ ...base, maitre: 0 }).volume, 0);
  assert.equal(calculerAudio(base).volume, 0.8);
});

test('le mute général coupe tout le monde, le mute individuel un seul', () => {
  assert.equal(calculerAudio({ ...base, muetMaitre: true }).muet, true);
  assert.equal(calculerAudio({ ...base, muetIndividuel: true }).muet, true);
  assert.equal(calculerAudio(base).muet, false);
});

test('le volume reste entre 0 et 1', () => {
  assert.equal(calculerAudio({ ...base, individuel: 3, maitre: 1 }).volume, 1);
  assert.equal(calculerAudio({ ...base, individuel: -1 }).volume, 0);
});

test('le volume général se lit, se borne et rétablit le son en l’écrivant', async () => {
  const magasin = new Map();
  globalThis.localStorage = { getItem: (k) => magasin.get(k) ?? null, setItem: (k, v) => magasin.set(k, v) };
  const { volumeMaitre, fixerVolumeMaitre } = await import('../../ui/js/son/volume-maitre.js');
  assert.equal(volumeMaitre(), 0.8);
  magasin.set('mu-muet', '1');
  fixerVolumeMaitre(1.7);
  assert.equal(volumeMaitre(), 1);
  assert.equal(magasin.get('mu-muet'), '0');
  fixerVolumeMaitre(0.25);
  assert.equal(volumeMaitre(), 0.25);
});
