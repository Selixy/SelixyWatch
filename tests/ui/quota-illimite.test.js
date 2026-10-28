import test from 'node:test';
import assert from 'node:assert/strict';
import { texteQuota, illimite } from '../../ui/js/login/quota.js';
import { etatOffre } from '../../ui/js/login/offre-etat.js';

test('un quota nul s\'affiche illimité', () => {
  assert.equal(illimite({ quota: null }), true);
  assert.equal(illimite({ quota: 0 }), false);
  assert.equal(texteQuota({ utilise: 2048, quota: null }), '2,0 Ko utilisés · illimité');
  assert.equal(texteQuota({ utilise: 1024, quota: 2048 }), '1,0 Ko utilisés sur 2,0 Ko');
});

test('l\'administrateur voit sa carte Offre dédiée', () => {
  const etat = etatOffre({ admin: true, offre: 'pro', envoi_fichiers: true });
  assert.equal(etat.titre, 'Administrateur · stockage illimité');
  assert.equal(etat.jauge, true);
  assert.equal(etat.note, null);
});
