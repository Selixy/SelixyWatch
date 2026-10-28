import { surChangement } from '../etat.js';
import { initSession } from '../session.js';
import { elements } from './contexte.js';
import { message } from './messages.js';
import { initSon } from './reglages-son.js';
import { initCinema } from './cinema.js';
import { initCommandes } from './commandes.js';
import { initDeblocage } from './deblocage.js';
import { initPointeur } from './pointeur.js';
import { initBarre, tic } from './progression.js';
import { initFile } from './file.js';
import { initClavier } from './clavier.js';
import { initPlein } from './plein.js';
import { initChatPlein } from './chat-plein.js';
import { initSynchro } from './synchro.js';
import { initDisposition } from './disposition.js';
import { repos } from './repos.js';
import { majAffichage } from './affichage.js';
import { initPreparation } from './preparation.js';

function activerDiagnostic() {
  try {
    if (/[?&]debug\b/.test(window.top.location.search)) import('../debug.js').then((m) => m.activerDebug(elements.ecran));
  } catch { return; }
}

export function initLecteur() {
  initSon();
  initCinema();
  initCommandes();
  initDeblocage();
  initPointeur();
  initBarre();
  initFile();
  initClavier();
  initPlein();
  initChatPlein();
  initSession();
  initSynchro();
  initDisposition();
  activerDiagnostic();
  setInterval(repos, 400);
  surChangement((quoi) => { if (quoi === 'canal' || quoi === 'arbre') { message(''); majAffichage(); } });
  majAffichage();
  tic();
  initPreparation();
}
