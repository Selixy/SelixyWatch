import { $, esc, duree, icone } from '../ui.js';
import { api } from '../api.js';
import { champ, listeRes } from './elements.js';
import { P, message } from './page.js';
import { lienReconnu, ajouterLien } from './liens.js';

let jeton = 0, minuteur = 0;

export function fermerResultats() {
  jeton++; clearTimeout(minuteur); listeRes.hidden = true; listeRes.innerHTML = '';
}

function afficherResultats(res) {
  listeRes.innerHTML = res.length
    ? res.map((r) => `<li><button type="button" class="resultat" data-yt="${esc(r.yt)}"><span class="vignette"><img src="https://i.ytimg.com/vi/${esc(r.yt)}/mqdefault.jpg" alt="" loading="lazy"></span>` +
      `<span class="res-texte"><span class="res-nom">${esc(r.nom)}</span><span class="res-auteur">${esc(r.auteur)}</span></span>` +
      `<span class="res-duree">${duree(r.duree)}</span><span class="res-plus">${icone('plus', 16)}</span></button></li>`).join('')
    : '<li class="res-vide">Aucun résultat</li>';
  listeRes.hidden = false;
}

async function chercher(q) {
  const mien = ++jeton;
  const r = await api('/api/recherche?q=' + encodeURIComponent(q));
  if (mien !== jeton) return;
  if (!r.ok) return message(r.data?.erreur || 'Recherche impossible.');
  message('');
  afficherResultats(r.data?.resultats || []);
}

async function ajouterResultat(e) {
  const b = e.target.closest('[data-yt]');
  if (!b || b.classList.contains('ajoute')) return;
  b.classList.add('ajoute');
  b.querySelector('.res-plus').innerHTML = icone('coche', 16);
  if (!await ajouterLien(`https://www.youtube.com/watch?v=${b.dataset.yt}`, P.vue, false)) {
    b.classList.remove('ajoute');
    b.querySelector('.res-plus').innerHTML = icone('plus', 16);
  }
}

export function brancherRecherche() {
  champ.addEventListener('input', () => {
    clearTimeout(minuteur);
    const q = champ.value.trim();
    if (q.length < 2 || lienReconnu(q)) { fermerResultats(); return; }
    minuteur = setTimeout(() => chercher(q), 400);
  });
  champ.addEventListener('paste', () => setTimeout(() => { if (lienReconnu(champ.value.trim())) $('#lien').requestSubmit(); }));
  champ.addEventListener('keydown', (e) => { if (e.key === 'Escape') fermerResultats(); });
  $('#lien').addEventListener('submit', (e) => {
    e.preventDefault();
    const q = champ.value.trim();
    if (!q) return;
    clearTimeout(minuteur);
    if (lienReconnu(q)) { fermerResultats(); ajouterLien(q, P.vue, true); } else chercher(q);
  });
  listeRes.addEventListener('click', ajouterResultat);
  document.addEventListener('click', (e) => { if (!listeRes.hidden && !e.target.closest('.ajout')) fermerResultats(); });
}
