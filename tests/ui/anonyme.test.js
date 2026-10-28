import test from 'node:test';
import assert from 'node:assert/strict';
import { creerAnonyme, confirmerDeconnexion, AVERTISSEMENT } from '../../ui/js/invitation/anonyme.js';

test('creerAnonyme renvoie le profil ou l\'erreur du serveur', async () => {
  const appels = [];
  const bon = async (...a) => { appels.push(a); return { ok: true, status: 201, data: { pseudo: 'Invité-1234', ephemere: true } }; };
  assert.equal((await creerAnonyme(bon)).profil.pseudo, 'Invité-1234');
  assert.deepEqual(appels[0], ['/api/anonyme', { method: 'POST' }]);
  const mauvais = async () => ({ ok: false, status: 429, data: { erreur: 'Trop de comptes.' } });
  assert.equal((await creerAnonyme(mauvais)).erreur, 'Trop de comptes.');
});

test('la déconnexion d\'un compte anonyme demande confirmation avec l\'avertissement', () => {
  const textes = [];
  assert.equal(confirmerDeconnexion({ ephemere: false }, () => assert.fail()), true);
  assert.equal(confirmerDeconnexion({ ephemere: true }, (t) => { textes.push(t); return false; }), false);
  assert.equal(confirmerDeconnexion({ ephemere: true }, () => true), true);
  assert.ok(textes[0].startsWith(AVERTISSEMENT));
});
