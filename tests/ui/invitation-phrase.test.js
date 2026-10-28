import test from 'node:test';
import assert from 'node:assert/strict';
import { destinationDe } from '../../ui/js/invitation/destination.js';
import { phrase } from '../../ui/js/invitation/phrase.js';

test('la phrase nomme l\'invitant et les éléments, sans rôle', () => {
  const dire = (...noms) => phrase({ par: { pseudo: 'Léa' }, noeuds: noms.map((nom) => ({ nom })) });
  assert.equal(dire('A'), 'Léa vous invite à A');
  assert.equal(dire('A', 'B'), 'Léa vous invite à A et B');
  assert.equal(dire('A', 'B', 'C'), 'Léa vous invite à A, B et 1 autre');
  assert.equal(dire('A', 'B', 'C', 'D', 'E'), 'Léa vous invite à A, B et 3 autres');
});

test('plusieurs éléments mènent à la vue Playlists, ouverte sur le premier', () => {
  const liste = [{ type: 'playlist', id: 'p1' }, { type: 'dossier', id: 'd1' }];
  assert.deepEqual(destinationDe(liste), { vue: 'playlists', cle: 'mu-dossier', id: 'p1' });
  assert.deepEqual(destinationDe([liste[0]]), { vue: 'room', cle: 'mu-canal', id: 'p1' });
});
