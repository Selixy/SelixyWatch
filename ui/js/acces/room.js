import { $ } from '../ui.js';
import { S, surChangement } from '../etat.js';

const MESSAGES = {
  anonyme: { titre: 'Connexion requise', texte: 'Connectez-vous pour rejoindre cette room.', lien: '/#profil', libelle: 'Se connecter' },
  refuse: { titre: 'Room inaccessible', texte: 'Cette room n\'existe plus ou vous n\'y avez plus accès.', lien: '/#playlists', libelle: 'Retour aux playlists' },
};

export const motifSansAcces = (etat) => (etat.anonyme ? 'anonyme' : etat.refuse ? 'refuse' : null);

export function afficherAcces() {
  const m = MESSAGES[motifSansAcces(S)];
  $('#sans-acces').hidden = !m;
  $('#salle').hidden = !!m;
  if (!m) return;
  $('#sans-acces h1').textContent = m.titre;
  $('#sans-acces p').textContent = m.texte;
  const lien = $('#sans-acces a');
  lien.href = m.lien;
  lien.textContent = m.libelle;
}

export function initAcces() {
  surChangement(afficherAcces);
  afficherAcces();
}
