import { S, noeud, peutModifier } from '../etat.js';
import { api } from '../api.js';
import { champ } from './elements.js';
import { P, message } from './page.js';

const RE_LIEN = /^https?:\/\/(?:[\w-]+\.)?(?:youtube\.com|youtu\.be|spotify\.com)\/\S+$/i;
const surLiens = new Set();

export const lienReconnu = (texte) => RE_LIEN.test((texte || '').trim());
export const saisissable = (el) => el?.closest?.('input, textarea, select, [contenteditable=""], [contenteditable="true"]');

export async function ajouterLien(url, playlist, viderChamp = true) {
  url = (url || '').trim();
  if (!url) return false;
  if (!playlist) { message('Choisissez d\'abord une playlist.'); return false; }
  if (!peutModifier(noeud(playlist))) { message('Vous ne pouvez pas modifier cette playlist.'); return false; }
  if (!lienReconnu(url)) { message('Lien non reconnu : YouTube ou Spotify.'); return false; }
  const r = await api('/api/liens', { method: 'POST', body: { url, playlist } });
  if (!r.ok) { message(r.data?.erreur || 'Ajout impossible.'); return false; }
  message('');
  if (viderChamp && playlist === P.vue) champ.value = '';
  return true;
}

export function erreursImport() {
  for (const [id, i] of Object.entries(S.imports)) {
    if (i.en_cours) { surLiens.delete(id); continue; }
    if (i.erreur && !surLiens.has(id)) { surLiens.add(id); message(id === P.vue || !noeud(id) ? i.erreur : `${noeud(id).nom} : ${i.erreur}`); }
  }
}

export function brancherCollage() {
  document.addEventListener('paste', (e) => {
    if (saisissable(e.target)) return;
    const t = (e.clipboardData?.getData('text') || '').trim();
    if (!lienReconnu(t)) return;
    e.preventDefault();
    ajouterLien(t, P.vue);
  });
}
