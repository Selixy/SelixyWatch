import { api } from '../api.js';
import { $ } from '../ui.js';
import { message } from './affichage.js';
import { ligneSession } from './sessions-rendu.js';
import { texteServeur } from './regles.js';
import { retourner, prevenirCoque } from './redirection.js';

const CIBLE = '#message-sessions';

export async function chargerSessions() {
  const r = await api('/api/moi/sessions');
  if (!r.ok) return message(texteServeur(r, 'Sessions illisibles.'), false, CIBLE);
  $('#liste-sessions').innerHTML = (r.data?.sessions || []).map(ligneSession).join('');
}

async function revoquer(e) {
  const ligne = e.target.closest('[data-revoquer]')?.closest('.session');
  if (!ligne) return;
  const r = await api('/api/moi/sessions/revoquer', { method: 'POST', body: { id: ligne.dataset.id } });
  if (!r.ok) return message(texteServeur(r, 'Révocation impossible.'), false, CIBLE);
  message('', false, CIBLE);
  chargerSessions();
}

async function partout() {
  const r = await api('/api/deconnexion/partout', { method: 'POST' });
  if (!r.ok) return message(texteServeur(r, 'Déconnexion impossible.'), false, CIBLE);
  prevenirCoque();
  retourner();
}

export function brancherSessions() {
  $('#liste-sessions').onclick = revoquer;
  $('#deconnexion-partout').onclick = partout;
  chargerSessions();
}
