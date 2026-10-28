import { $, esc } from '../ui.js';
import { noeud, peutModifier } from '../etat.js';
import { P, message } from './page.js';
import { envoyerMiniature } from './miniature.js';
import { droit } from './droit-envoi.js';
import { texteEchecEnvoi } from './messages-envoi.js';

const file = [];
let enCours = false;

function dureeFichier(f) {
  return new Promise((ok) => {
    const v = document.createElement('video'), u = URL.createObjectURL(f);
    const fin = (d) => { URL.revokeObjectURL(u); v.removeAttribute('src'); ok(Number.isFinite(d) ? d : 0); };
    v.preload = 'metadata'; v.onloadedmetadata = () => fin(v.duration); v.onerror = () => fin(0);
    v.src = u;
  });
}

function envoyerUn(f, playlist, barre) {
  return new Promise(async (ok) => {
    const x = new XMLHttpRequest();
    x.open('POST', '/api/medias');
    x.setRequestHeader('X-Nom', encodeURIComponent(f.name));
    x.setRequestHeader('X-Playlist', playlist);
    x.setRequestHeader('X-Duree', String(await dureeFichier(f)));
    x.upload.onprogress = (e) => { if (e.lengthComputable) barre.style.width = `${(e.loaded / e.total) * 100}%`; };
    x.onload = async () => {
      let d = {}; try { d = JSON.parse(x.responseText); } catch { d = {}; }
      if (x.status < 300) await envoyerMiniature(f, x.responseText);
      ok(x.status < 300 ? null : texteEchecEnvoi(x.status, d));
    };
    x.onerror = () => ok('Le serveur est injoignable.');
    x.send(f);
  });
}

export async function envoyer(fichiers, playlist) {
  if (!droit.autorise) return message('L\'envoi de fichiers n\'est pas disponible avec votre compte.');
  if (!peutModifier(noeud(playlist))) return message('Vous ne pouvez pas modifier cette playlist.');
  file.push(...fichiers.filter((f) => f.size).map((f) => ({ f, playlist })));
  if (enCours) return;
  enCours = true;
  const zone = $('#envois');
  while (file.length) {
    const { f, playlist: p } = file.shift();
    const li = document.createElement('li');
    li.innerHTML = `<span class="nom">${esc(f.name)}</span><span class="progres"><i></i></span><span class="note"></span>`;
    zone.append(li);
    const err = await envoyerUn(f, p, li.querySelector('i'));
    if (err) { li.querySelector('.note').textContent = err; li.classList.add('echec'); setTimeout(() => li.remove(), 8000); }
    else li.remove();
  }
  enCours = false;
}

export function brancherEnvoi() {
  $('#vue-importer').onclick = () => $('#fichiers').click();
  $('#fichiers').onchange = (e) => { if (P.vue) envoyer([...e.target.files], P.vue); e.target.value = ''; };
}
