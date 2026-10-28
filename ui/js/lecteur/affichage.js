import { $, icone } from '../ui.js';
import { S, etat, media, nom, ordre } from '../etat.js';
import { elements, courant } from './contexte.js';
import { majFile, precharger } from './file.js';
import { majPoster } from './poster.js';
import { repos } from './repos.js';
import { caler } from './synchro.js';

export function majAffichage() {
  const m = courant(), e = etat();
  const pistes = ordre(S.canal);
  elements.ecran.classList.toggle('audio', m?.genre === 'audio');
  elements.ecran.classList.toggle('vide', !m);
  $('#haut-titre').textContent = m ? `${nom(S.canal)} › ${m.nom}` : '';
  $('#ecran-nom').textContent = m && m.genre === 'audio' ? m.nom : '';
  $('#grand-lire').innerHTML = icone('play', 32);
  $('#grand-lire').classList.toggle('cache', !!m || !pistes.length);
  $('#lire').innerHTML = icone(e?.lecture ? 'pause' : 'play', 24);
  $('#lire').setAttribute('aria-label', e?.lecture ? 'Pause' : 'Lecture');
  for (const b of document.querySelectorAll('.act-prec, .act-suiv')) b.disabled = !m;
  $('#en-lecture').hidden = !m;
  $('#titre-lu').textContent = m ? m.nom : '';
  for (const cle of ['boucle', 'aleatoire']) $('#' + cle).setAttribute('aria-pressed', String(!!e?.[cle]));
  majFile();
  precharger();
  majPoster();
  repos();
  caler();
}
