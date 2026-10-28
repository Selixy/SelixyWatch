import test from 'node:test';
import assert from 'node:assert/strict';
import { analyserHash } from '../../ui/js/coque/ouverture.js';
import { lienComplet } from '../../ui/js/partager/lien.js';

test('le hash vue/identifiant est reconnu, un identifiant mal formé est ignoré', () => {
  assert.deepEqual(analyserHash('#playlists/0123456789ab'), { vue: 'playlists', id: '0123456789ab' });
  assert.deepEqual(analyserHash('#room/0123456789ab'), { vue: 'room', id: '0123456789ab' });
  assert.deepEqual(analyserHash('#playlists'), { vue: 'playlists', id: null });
  assert.deepEqual(analyserHash('#playlists/../x'), { vue: 'playlists', id: null });
});

test('le lien d\'invitation complet ajoute l\'origine', () => {
  assert.equal(lienComplet('https://watch.selixy.dev', '/invitation/#abc'), 'https://watch.selixy.dev/invitation/#abc');
});
