import { $, esc, duree, vignette } from '../ui.js';
import { S, etat, media, ordre, agir } from '../etat.js';
import { erreur } from './messages.js';

const precharges = new Map();

export function majFile() {
  const liste = (etat()?.suite ?? ordre(S.canal)).filter((id) => media(id));
  $('#suite').innerHTML = liste.map((id) => {
    const m = media(id);
    const cour = id === etat()?.courant;
    return `<li><button type="button" class="piste-file${cour ? ' courante' : ''}"${cour ? ' aria-current="true"' : ''} data-id="${esc(id)}">` +
      `<span class="vignette">${vignette(id, m, 28)}${m.duree ? `<span class="piste-duree">${duree(m.duree)}</span>` : ''}</span>` +
      `<span class="piste-nom">${esc(m.nom)}</span></button></li>`;
  }).join('');
}

export function precharger() {
  const prochains = (etat()?.suite ?? []).filter((id) => media(id) && !media(id).source).slice(0, 2);
  for (const [id, v] of precharges) if (!prochains.includes(id)) { v.removeAttribute('src'); v.load(); precharges.delete(id); }
  for (const id of prochains) {
    if (precharges.has(id)) continue;
    const m = media(id), v = document.createElement('video');
    v.preload = 'auto'; v.muted = true; v.playsInline = true; v.src = `/medias/${id}.${m.ext}`; v.load();
    precharges.set(id, v);
    if (m.taille && m.taille <= 30e6 && !navigator.connection?.saveData) fetch(v.src).then((r) => r.arrayBuffer()).catch(() => {});
  }
}

export function initFile() {
  $('#suite').addEventListener('click', (e) => {
    const b = e.target.closest('.piste-file');
    if (b) agir('jouer', { media: b.dataset.id }).catch(erreur);
  });
  for (const cle of ['boucle', 'aleatoire']) {
    $('#' + cle).onclick = () => agir(cle, { actif: !etat()?.[cle] }).catch(erreur);
  }
}
