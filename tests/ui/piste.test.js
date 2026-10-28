import test from 'node:test';
import assert from 'node:assert/strict';
import { creerPiste } from '../../ui/js/lecteur/flux/piste.js';
import { construireEntete, TAILLE_SEGMENT } from './mp4-factice.js';
import { TamponFactice } from './tampon-factice.js';

const NOMBRE = 8;
const entete = construireEntete(NOMBRE);

async function lireFactice(adresse, debut, fin) {
  if (debut === 0) return entete;
  return new Uint8Array(fin - debut + 1).fill((debut - entete.length) / TAILLE_SEGMENT);
}

async function preparerPiste() {
  const tampon = new TamponFactice();
  const piste = creerPiste(tampon, '/flux/x/video', lireFactice);
  await piste.preparer();
  return { tampon, piste };
}

test('prépare en ajoutant le segment d\'initialisation', async () => {
  const { tampon } = await preparerPiste();
  assert.deepEqual(tampon.ajouts, ['init']);
});

test('charge les segments nécessaires à partir de la position', async () => {
  const { tampon, piste } = await preparerPiste();
  await piste.assurer(0, 12);
  assert.deepEqual(tampon.ajouts.slice(1), [0, 1, 2]);
  assert.equal(piste.fini(), false);
});

test('ne recharge pas ce qui est déjà en mémoire', async () => {
  const { tampon, piste } = await preparerPiste();
  await piste.assurer(0, 12);
  await piste.assurer(1, 12);
  assert.deepEqual(tampon.ajouts.slice(1), [0, 1, 2]);
  await piste.assurer(5, 12);
  assert.deepEqual(tampon.ajouts.slice(1), [0, 1, 2, 3]);
});

test('après un saut, repart du segment visé', async () => {
  const { tampon, piste } = await preparerPiste();
  await piste.assurer(0, 5);
  await piste.assurer(30, 6);
  assert.deepEqual(tampon.ajouts.slice(1), [0, 6, 7]);
  assert.equal(piste.fini(), true);
});
