import { api } from '../api.js';
import { $ } from '../ui.js';
import { afficherCompte } from '../compte.js';
import { saisie } from './saisie.js';
import { message, apercu } from './affichage.js';
import { prevenirCoque } from './redirection.js';
import { texteServeur } from './regles.js';

async function envoyerAvatar() {
  const rep = await fetch('/api/moi/avatar', { method: 'POST', credentials: 'same-origin', headers: { 'Content-Type': saisie.image.type }, body: saisie.image });
  const d = await rep.json().catch(() => ({}));
  if (!rep.ok) { message(d.erreur || 'Envoi de l\'avatar impossible.'); return false; }
  saisie.profil = d;
  saisie.image = null;
  return true;
}

async function appliquerAvatar() {
  if (saisie.image) return envoyerAvatar();
  if (saisie.retirer) {
    await api('/api/moi/avatar/supprimer', { method: 'POST' });
    saisie.profil = { ...saisie.profil, avatar: null };
    saisie.retirer = false;
  }
  return true;
}

async function enregistrer(pseudo) {
  const r = await api('/api/moi', { method: 'POST', body: { pseudo } });
  if (!r.ok) return message(texteServeur(r, 'Enregistrement impossible.'));
  saisie.profil = r.data;
  if (!(await appliquerAvatar())) return;
  afficherCompte(saisie.profil);
  prevenirCoque();
  apercu();
  message('Enregistré.', true);
}

export async function soumettre(e) {
  e.preventDefault();
  const pseudo = $('#pseudo').value.trim();
  if (pseudo.length < 2) return message('Le pseudo doit contenir au moins 2 caractères.');
  $('#enregistrer').disabled = true;
  try {
    await enregistrer(pseudo);
  } finally {
    $('#enregistrer').disabled = false;
  }
}
