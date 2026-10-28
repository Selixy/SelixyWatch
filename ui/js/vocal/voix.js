import { creerAnalyseur, mesurerNiveau, libererAnalyseur } from './voix-analyse.js';

const SEUIL_PAROLE = 0.08;
const MONTEE = 0.5;
const DESCENTE = 0.12;

const suivis = new Map();
let image = 0;

function appliquer(id, suivi, niveau) {
  const el = document.querySelector(`.present[data-id="${CSS.escape(id)}"]`);
  if (!el) return;
  suivi.lisse += (niveau - suivi.lisse) * (niveau > suivi.lisse ? MONTEE : DESCENTE);
  el.style.setProperty('--voix', suivi.lisse.toFixed(3));
  el.classList.toggle('parle', suivi.lisse > SEUIL_PAROLE);
}

function boucle() {
  for (const [id, suivi] of suivis) appliquer(id, suivi, mesurerNiveau(suivi.analyseur));
  image = suivis.size ? requestAnimationFrame(boucle) : 0;
}

export function suivreVoix(id, piste) {
  oublierVoix(id);
  suivis.set(id, { analyseur: creerAnalyseur(piste), lisse: 0 });
  if (!image) image = requestAnimationFrame(boucle);
}

export function oublierVoix(id) {
  const suivi = suivis.get(id);
  if (!suivi) return;
  libererAnalyseur(suivi.analyseur);
  suivis.delete(id);
  const el = document.querySelector(`.present[data-id="${CSS.escape(id)}"]`);
  el?.style.removeProperty('--voix');
  el?.classList.remove('parle');
}
