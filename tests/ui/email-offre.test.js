import test from 'node:test';
import assert from 'node:assert/strict';
import { etatEmail, erreurEmail, texteEmail } from '../../ui/js/login/email-etat.js';
import { etatOffre } from '../../ui/js/login/offre-etat.js';
import { erreurNouveau } from '../../ui/js/login/regles.js';
import { texteConfirmation, confirmer } from '../../ui/js/confirmer/appel.js';
import { texteRecuperation, renouveler } from '../../ui/js/recuperation/appel.js';
import { mentionEnvoi, texteEchecEnvoi } from '../../ui/js/playlists/messages-envoi.js';
import { lireJeton } from '../../ui/js/invitation/jeton.js';

test('la carte e-mail distingue aucune adresse, en attente et validée', () => {
  assert.equal(etatEmail({ email: null, email_valide: false, email_en_attente: null }).mode, 'aucun');
  const attente = etatEmail({ email: null, email_valide: false, email_en_attente: 'a@b.fr' });
  assert.equal(attente.mode, 'attente');
  assert.equal(attente.texte, 'En attente de validation : a@b.fr');
  assert.equal(etatEmail({ email: 'a@b.fr', email_valide: true, email_en_attente: null }).mode, 'valide');
});

test('la saisie de l\'e-mail exige une adresse valide et le mot de passe', () => {
  assert.match(erreurEmail('pas-une-adresse', 'x'), /valide/);
  assert.match(erreurEmail('a@b.fr', ''), /mot de passe/);
  assert.equal(erreurEmail('a@b.fr', 'x'), null);
  assert.match(texteEmail({ status: 409 }), /déjà validée/);
  assert.equal(texteEmail({ status: 500, data: { erreur: 'Boum' } }), 'Boum');
});

test('la carte offre dit Free, Pro validé ou Pro sans e-mail validé', () => {
  const free = etatOffre({ offre: 'free', envoi_fichiers: false });
  assert.equal(free.jauge, false);
  assert.match(free.note, /réservé aux comptes Pro/);
  assert.deepEqual(etatOffre({ offre: 'pro', envoi_fichiers: true }), { titre: 'Offre Pro', note: null, jauge: true });
  assert.match(etatOffre({ offre: 'pro', envoi_fichiers: false }).note, /Validez votre adresse e-mail/);
});

test('la mention d\'envoi dépend de l\'offre et de l\'envoi autorisé', () => {
  assert.equal(mentionEnvoi({ offre: 'pro', envoi_fichiers: true }), null);
  assert.deepEqual(mentionEnvoi({ offre: 'free', envoi_fichiers: false }), { texte: 'Envoi de fichiers : offre Pro', lien: null });
  assert.deepEqual(mentionEnvoi({ offre: 'pro', envoi_fichiers: false }), { texte: 'Validez votre e-mail', lien: '/#profil' });
});

test('les échecs d\'envoi 402, 403 et 507 ont leur message', () => {
  assert.match(texteEchecEnvoi(402, {}), /réservé aux comptes Pro/);
  assert.match(texteEchecEnvoi(403, {}), /Validez votre adresse/);
  assert.match(texteEchecEnvoi(507, {}), /plein/);
  assert.equal(texteEchecEnvoi(500, { erreur: 'Zut' }), 'Zut');
});

test('le jeton se lit dans le hash et les pages traduisent 410 et 409', async () => {
  assert.equal(lireJeton('#abcdefgh12345'), 'abcdefgh12345');
  assert.equal(lireJeton('#x'), null);
  assert.match(texteConfirmation(410), /expiré/);
  assert.match(texteConfirmation(409), /autre compte/);
  assert.match(texteRecuperation(410), /expiré/);
  const faux = async () => ({ ok: true, status: 200, data: { email: 'a@b.fr' } });
  assert.deepEqual(await confirmer(faux, 'jeton1234'), { email: 'a@b.fr' });
  assert.deepEqual(await renouveler(faux, 'jeton1234', 'nouveaumdp'), {});
  const refus = async () => ({ ok: false, status: 410, data: null });
  assert.match((await confirmer(refus, 'j')).erreur, /expiré/);
});

test('le nouveau mot de passe exige 8 caractères et une confirmation', () => {
  assert.equal(erreurNouveau({ nouveau: 'motdepasse', confirmation: 'motdepasse' }), null);
  assert.match(erreurNouveau({ nouveau: 'court', confirmation: 'court' }), /8 caractères/);
  assert.match(erreurNouveau({ nouveau: 'motdepasse', confirmation: 'autre' }), /correspondent/);
});
