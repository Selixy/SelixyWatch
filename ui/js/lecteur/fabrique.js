import { elements } from './contexte.js';
import { creerLecteurFichier } from './fichier.js';
import { creerLecteurYoutube } from './youtube.js';

export const fichier = creerLecteurFichier(elements);
export const yt = creerLecteurYoutube(elements.ecran);
export const lecteurs = [fichier, yt];

export const lecteurDe = (m) => (!m ? null : m.source === 'youtube' ? yt : fichier);
