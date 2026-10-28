import { api } from '../api.js';
import { $ } from '../ui.js';
import { message } from './affichage.js';
import { mode } from './mode.js';
import { erreurSaisie, texteServeur } from './regles.js';
import { terminerConnexion } from './suite-connexion.js';

const lire = () => ({
  pseudo: $('#pseudo-auth').value.trim(),
  mdp: $('#mdp').value,
  confirmation: $('#confirmation').value,
});

async function envoyer(saisieAuth) {
  const chemin = mode.courant === 'inscription' ? '/api/inscription' : '/api/connexion';
  const r = await api(chemin, { method: 'POST', body: { pseudo: saisieAuth.pseudo, mdp: saisieAuth.mdp } });
  if (!r.ok) return message(texteServeur(r, 'Connexion impossible.'), false, '#message-auth');
  await terminerConnexion(r.data);
}

export async function soumettreAuth(e) {
  e.preventDefault();
  const s = lire();
  const erreur = erreurSaisie(mode.courant, s);
  if (erreur) return message(erreur, false, '#message-auth');
  $('#valider-auth').disabled = true;
  try {
    await envoyer(s);
  } finally {
    $('#valider-auth').disabled = false;
  }
}
