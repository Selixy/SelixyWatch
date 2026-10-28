import { $ } from '../ui.js';
import { deconnecter } from '../compte.js';
import { retourner } from './redirection.js';
import { afficherOffre } from './offre.js';
import { brancherEmail } from './email.js';
import { brancherMdp } from './mdp.js';
import { brancherSessions } from './sessions.js';
import { brancherSuppression } from './suppression.js';
import { AVERTISSEMENT, confirmerDeconnexion } from '../invitation/anonyme.js';

function montrerSections(ephemere) {
  for (const el of document.querySelectorAll('[data-connecte]')) el.hidden = ephemere && 'permanent' in el.dataset;
  $('#bandeau-anonyme').hidden = !ephemere;
  $('#bandeau-anonyme').textContent = AVERTISSEMENT;
}

export function montrerProfil(profil) {
  $('#pseudo').value = profil.pseudo;
  $('#titre-page').textContent = 'Profil';
  document.title = 'Profil · SelixyWatch';
  $('#deconnexion').onclick = async () => {
    if (!confirmerDeconnexion(profil, (t) => window.confirm(t))) return;
    await deconnecter();
    retourner();
  };
  montrerSections(!!profil.ephemere);
  $('#auth').hidden = true;
  afficherOffre(profil);
  if (profil.ephemere) return brancherSuppression();
  brancherEmail(profil);
  brancherMdp();
  brancherSessions();
  brancherSuppression();
}
