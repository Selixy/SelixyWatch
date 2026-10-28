import { api } from '../api.js';
import { $ } from '../ui.js';
import { moi } from '../compte.js';
import { message } from './affichage.js';
import { etatEmail, erreurEmail, texteEmail } from './email-etat.js';
import { afficherOffre } from './offre.js';

const CIBLE = '#message-email';

function afficher(profil) {
  const etat = etatEmail(profil);
  $('#email-etat').textContent = etat.texte;
  $('#email-renvoyer').hidden = etat.mode !== 'attente';
  $('#email-retirer').hidden = etat.mode === 'aucun';
  $('#email-adresse').value = etat.adresse;
  afficherOffre(profil);
}

async function actualiser(texte) {
  $('#mdp-email').value = '';
  afficher(await moi());
  message(texte, true, CIBLE);
}

async function enregistrer(e) {
  e.preventDefault();
  const adresse = $('#email-adresse').value.trim(), mdp = $('#mdp-email').value;
  const erreur = erreurEmail(adresse, mdp);
  if (erreur) return message(erreur, false, CIBLE);
  const r = await api('/api/moi/email', { method: 'POST', body: { email: adresse, mdp } });
  if (!r.ok) return message(texteEmail(r), false, CIBLE);
  await actualiser(r.data?.envoye === false ? 'Adresse enregistrée, mais le lien n\'a pas pu partir. Utilisez « Renvoyer le lien ».' : 'Un lien de validation vient de partir.');
}

async function retirer() {
  const mdp = $('#mdp-email').value;
  if (!mdp) return message('Saisissez votre mot de passe pour confirmer.', false, CIBLE);
  const r = await api('/api/moi/email/supprimer', { method: 'POST', body: { mdp } });
  if (!r.ok) return message(texteEmail(r), false, CIBLE);
  await actualiser('Adresse retirée.');
}

export function brancherEmail(profil) {
  afficher(profil);
  $('#form-email').onsubmit = enregistrer;
  $('#email-renvoyer').onclick = enregistrer;
  $('#email-retirer').onclick = retirer;
}
