import test from 'node:test';
import assert from 'node:assert/strict';
import { peutModifier, estProprietaire, estRacineRecue, peutDeplacer, peutRenommer } from '../../ui/js/etat/droits.js';
import { deplacementPermis, parentDeCreation } from '../../ui/js/etat/droits-arbre.js';

const noeuds = [
  { id: 'd1', parent: 'racine', type: 'dossier', role: 'proprietaire' },
  { id: 'p1', parent: 'd1', type: 'playlist', role: 'proprietaire' },
  { id: 'r1', parent: 'racine', type: 'dossier', role: 'editeur', partage_racine: true },
  { id: 'r2', parent: 'd1', type: 'dossier', role: 'lecteur', partage_racine: true },
  { id: 'e1', parent: 'r1', type: 'playlist', role: 'editeur' },
];
const noeud = (id) => noeuds.find((n) => n.id === id);

test('seuls propriétaire et éditeur modifient', () => {
  assert.ok(peutModifier(noeud('d1')) && peutModifier(noeud('r1')));
  assert.ok(!peutModifier(noeud('r2')) && !peutModifier(undefined));
  assert.ok(estProprietaire(noeud('p1')) && !estProprietaire(noeud('r1')));
});

test('déplacer et renommer sont permis sur tout élément visible, même en lecture seule', () => {
  for (const n of noeuds) assert.ok(peutDeplacer(n) && peutRenommer(n));
  assert.ok(!peutDeplacer(undefined) && !peutRenommer(undefined));
});

test('une racine de partage garde « Quitter » où qu\'elle soit rangée', () => {
  assert.ok(estRacineRecue(noeud('r1')) && estRacineRecue(noeud('r2')) && !estRacineRecue(noeud('e1')));
});

test('le déplacement croise librement mes dossiers et les dossiers reçus', () => {
  assert.ok(deplacementPermis(noeud('p1'), 'r1', noeud));
  assert.ok(deplacementPermis(noeud('e1'), 'd1', noeud));
  assert.ok(deplacementPermis(noeud('r2'), 'racine', noeud));
  assert.ok(deplacementPermis(noeud('e1'), 'racine', noeud));
  assert.ok(!deplacementPermis(noeud('p1'), 'e1', noeud));
  assert.ok(!deplacementPermis(noeud('p1'), 'inconnu', noeud));
});

test('la création se fait à la racine quand la sélection n\'est pas modifiable', () => {
  assert.equal(parentDeCreation('d1', noeud), 'd1');
  assert.equal(parentDeCreation('p1', noeud), 'd1');
  assert.equal(parentDeCreation('r1', noeud), 'r1');
  assert.equal(parentDeCreation('r2', noeud), 'racine');
  assert.equal(parentDeCreation('e1', noeud), 'r1');
});
