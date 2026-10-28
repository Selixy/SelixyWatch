import test from 'node:test';
import assert from 'node:assert/strict';
import { lireReponse } from '../../ui/js/etat/construction.js';

const propre = { id: 'a1', parent: 'racine', type: 'playlist', nom: 'A', role: 'proprietaire' };
const recu = { id: 'b1', parent: 'racine', type: 'dossier', nom: 'B', role: 'lecteur', partage_racine: true };

test('aucune racine virtuelle : les nœuds reçus sont rendus tels quels', () => {
  const lu = lireReponse(200, { noeuds: [propre, recu], medias: {} });
  assert.deepEqual(lu.noeuds.map((n) => n.id), ['a1', 'b1']);
  assert.ok(!lu.noeuds.some((n) => n.virtuel));
});

test('une réponse 401 donne un état anonyme, une erreur réseau ne change rien', () => {
  assert.deepEqual(lireReponse(401, null), { anonyme: true, noeuds: [], medias: {} });
  assert.equal(lireReponse(0, null), null);
  assert.equal(lireReponse(500, {}), null);
  const lu = lireReponse(200, { noeuds: [recu], medias: { m: 1 } });
  assert.equal(lu.anonyme, false);
  assert.equal(lu.noeuds.length, 1);
});
