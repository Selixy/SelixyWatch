import test from 'node:test';
import assert from 'node:assert/strict';
import { erreurSaisie, erreurChangement, texteServeur } from '../../ui/js/login/regles.js';
import { formaterOctets, pourcentage } from '../../ui/js/login/quota.js';
import { appareil } from '../../ui/js/login/sessions-rendu.js';

test('l\'inscription exige 8 caractères et une confirmation identique', () => {
  const base = { pseudo: 'Léa', mdp: 'motdepasse', confirmation: 'motdepasse' };
  assert.equal(erreurSaisie('inscription', base), null);
  assert.match(erreurSaisie('inscription', { ...base, mdp: 'court', confirmation: 'court' }), /8 caractères/);
  assert.match(erreurSaisie('inscription', { ...base, confirmation: 'autre' }), /correspondent/);
  assert.match(erreurSaisie('inscription', { ...base, pseudo: 'L' }), /pseudo/);
});

test('la connexion ne demande ni confirmation ni longueur', () => {
  assert.equal(erreurSaisie('connexion', { pseudo: 'Léa', mdp: 'x', confirmation: '' }), null);
  assert.ok(erreurSaisie('connexion', { pseudo: 'Léa', mdp: '', confirmation: '' }));
  assert.ok(erreurChangement({ ancien: '', nouveau: 'motdepasse', confirmation: 'motdepasse' }));
  assert.ok(erreurChangement({ ancien: 'a', nouveau: 'court', confirmation: 'court' }));
  assert.equal(erreurChangement({ ancien: 'a', nouveau: 'motdepasse', confirmation: 'motdepasse' }), null);
});

test('le message du serveur est affiché tel quel, avec repli pour 429', () => {
  assert.equal(texteServeur({ status: 409, data: { erreur: 'Ce pseudo est déjà pris.' } }, 'x'), 'Ce pseudo est déjà pris.');
  assert.match(texteServeur({ status: 429, data: null }, 'x'), /Trop de tentatives/);
  assert.equal(texteServeur({ status: 500, data: null }, 'défaut'), 'défaut');
});

test('les octets, le quota et l\'appareil se formatent', () => {
  assert.equal(formaterOctets(0), '0 o');
  assert.equal(formaterOctets(1536), '1,5 Ko');
  assert.equal(formaterOctets(5 * 1024 ** 3), '5,0 Go');
  assert.equal(pourcentage(50, 200), 25);
  assert.equal(pourcentage(500, 200), 100);
  assert.equal(appareil('Mozilla/5.0 (X11; Linux x86_64) Gecko/20100101 Firefox/130.0'), 'Firefox sur Linux');
  assert.equal(appareil(''), 'Appareil inconnu');
});
