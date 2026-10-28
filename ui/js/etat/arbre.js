import { S } from './partage.js';

export const noeud = (id) => S.noeuds.find((n) => n.id === id);
export const media = (id) => S.medias[id];
export const enfants = (pid) => S.noeuds.filter((n) => n.parent === pid);
export const estDossier = (id) => id === 'racine' || noeud(id)?.type === 'dossier';
export const estPlaylist = (id) => noeud(id)?.type === 'playlist';
