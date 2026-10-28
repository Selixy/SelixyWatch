import test from 'node:test';
import assert from 'node:assert/strict';
import { destination, entrerDans } from '../../ui/js/invitation/destination.js';
import { accepter, texteErreur } from '../../ui/js/invitation/acceptation.js';

const stockage = () => {
  const m = new Map();
  return { setItem: (k, v) => m.set(k, v), getItem: (k) => m.get(k) ?? null };
};

test('une playlist mène à sa room, un dossier à la vue Playlists', () => {
  assert.deepEqual(destination({ type: 'playlist', id: 'p1' }), { vue: 'room', cle: 'mu-canal', id: 'p1' });
  assert.deepEqual(destination({ type: 'dossier', id: 'd1' }), { vue: 'playlists', cle: 'mu-dossier', id: 'd1' });
});

test('entrer dans le site : message à la coque depuis un cadre, adresse sinon', () => {
  const s = stockage();
  const envoyes = [];
  const parent = { postMessage: (m) => envoyes.push(m) };
  entrerDans([{ type: 'playlist', id: 'p1' }], { stockage: s, cadre: true, parent, aller: () => assert.fail() });
  entrerDans([{ type: 'dossier', id: 'd1' }], { stockage: s, cadre: true, parent, aller: () => assert.fail() });
  assert.deepEqual(envoyes, [{ type: 'entrer', id: 'p1' }, { type: 'recharger', vue: 'playlists' }]);
  assert.equal(s.getItem('mu-canal'), 'p1');
  assert.equal(s.getItem('mu-dossier'), 'd1');
  const urls = [];
  entrerDans([{ type: 'playlist', id: 'p2' }], { stockage: s, cadre: false, parent, aller: (u) => urls.push(u) });
  assert.deepEqual(urls, ['/#room']);
});

test('accepter renvoie les nœuds, ou un texte propre pour 401, 404 et 410', async () => {
  const noeuds = [{ id: 'n', type: 'dossier' }];
  const bon = async () => ({ ok: true, status: 200, data: { noeuds, deja: true } });
  assert.deepEqual(await accepter(bon, 'j'), { noeuds, deja: true });
  for (const st of [401, 404, 410]) {
    const mauvais = async () => ({ ok: false, status: st, data: { erreur: 'brut' } });
    assert.equal((await accepter(mauvais, 'j')).erreur, texteErreur(st, null));
  }
  assert.equal(texteErreur(500, { erreur: 'Panne.' }), 'Panne.');
});
