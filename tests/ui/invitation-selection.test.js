import test from 'node:test';
import assert from 'node:assert/strict';
import { couverts, hauts } from '../../ui/js/partager/selection.js';
import { mesNoeuds, basculer } from '../../ui/js/partager/propres.js';
import { htmlArbreCases } from '../../ui/js/partager/rendu-inviter.js';
import { idsADeplier } from '../../ui/js/playlists/ouverture-chemin.js';

const n = (id, parent, type = 'dossier', role = 'proprietaire') => ({ id, parent, type, nom: id, role });
const noeuds = [n('d1', 'racine'), n('p1', 'd1', 'playlist'), n('d2', 'd1'), n('p2', 'd2', 'playlist'), n('p3', 'racine', 'playlist'),
  n('r1', 'racine', 'dossier', 'editeur')];

test('seuls mes éléments sont proposés', () => {
  assert.deepEqual(mesNoeuds(noeuds).map((x) => x.id), ['d1', 'p1', 'd2', 'p2', 'p3']);
});

test('cocher un dossier couvre tout son contenu', () => {
  assert.deepEqual([...couverts(mesNoeuds(noeuds), new Set(['d1']))].sort(), ['d2', 'p1', 'p2']);
});

test('seuls les ids de plus haut niveau sont envoyés', () => {
  const mien = mesNoeuds(noeuds);
  assert.deepEqual(hauts(mien, new Set(['p2', 'd1', 'p3'])).sort(), ['d1', 'p3']);
  assert.deepEqual(hauts(mien, basculer(new Set(['d1', 'p3']), 'd1', false)), ['p3']);
});

test('le contenu d\'un dossier coché est coché et grisé', () => {
  const html = htmlArbreCases(noeuds, new Set(['d1']));
  assert.match(html, /data-id="p2" checked disabled/);
  assert.match(html, /data-id="p3">/);
  assert.doesNotMatch(html, /data-id="r1"/);
});

test('un dossier reçu se déplie lui-même avec ses ancêtres', () => {
  const trouver = (id) => noeuds.find((x) => x.id === id);
  assert.deepEqual(idsADeplier(trouver('r1'), trouver), ['r1']);
  assert.deepEqual(idsADeplier(trouver('p2'), trouver), ['d2', 'd1']);
});
