import test from 'node:test';
import assert from 'node:assert/strict';
import { decider, DELAI_MS, ABANDON_MS } from '../../ui/js/lecteur/preparation-etapes.js';

const neuf = () => ({ debut: 0, pose: 0, voile: null, fini: false });

test('prête dès le début : rien à montrer', () => {
  assert.equal(decider(neuf(), true, 1000), 'terminer');
});

test("le voile n'apparaît qu'après le délai", () => {
  const p = neuf();
  assert.equal(decider(p, false, 1000), 'demarrer');
  p.debut = 1000;
  assert.equal(decider(p, false, 1000 + DELAI_MS - 1), 'attendre');
  assert.equal(decider(p, false, 1000 + DELAI_MS), 'poser');
});

test('une fois posé, le voile part dès que le lecteur est prêt, sans durée minimale', () => {
  const p = { debut: 1000, pose: 2000, voile: {}, fini: false };
  assert.equal(decider(p, true, 2001), 'retirer');
});

test("on abandonne si ce n'est jamais prêt", () => {
  assert.equal(decider({ debut: 1000, pose: 0, voile: null, fini: false }, false, 1000 + ABANDON_MS), 'terminer');
  assert.equal(decider({ debut: 1000, pose: 1700, voile: {}, fini: false }, false, 1000 + ABANDON_MS), 'retirer');
});

test('rien après la fin', () => {
  assert.equal(decider({ ...neuf(), fini: true }, false, 5), 'rien');
});

test('YouTube : prêt seulement quand YouTube a chargé la vidéo, pas dès l\'envoi de la commande', async () => {
  const { lecteurEstPret } = await import('../../ui/js/lecteur/preparation-etapes.js');
  const youtube = (etat) => ({ pret: () => true, preparee: () => [1, 2, 5].includes(etat) });
  [-1, 3].forEach((etat) => assert.equal(lecteurEstPret(youtube(etat), false), false));
  [1, 2, 5].forEach((etat) => assert.equal(lecteurEstPret(youtube(etat), false), true));
});

test('un fichier est prêt dès que son lecteur le dit, et un son bloqué par le navigateur ne retient pas le voile', async () => {
  const { lecteurEstPret } = await import('../../ui/js/lecteur/preparation-etapes.js');
  assert.equal(lecteurEstPret({ pret: () => false }, false), false);
  assert.equal(lecteurEstPret({ pret: () => true }, false), true);
  assert.equal(lecteurEstPret(({ pret: () => true, preparee: () => false }), true), true);
});
