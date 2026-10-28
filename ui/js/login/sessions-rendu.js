import { esc } from '../ui.js';

const SYSTEMES = [['Android', /Android/], ['iOS', /iPhone|iPad/], ['Windows', /Windows/], ['macOS', /Mac OS X/], ['Linux', /Linux/]];
const NAVIGATEURS = [['Edge', /Edg\//], ['Firefox', /Firefox\//], ['Chrome', /Chrome\/|CriOS/], ['Safari', /Safari\//]];

const trouver = (liste, agent) => liste.find(([, re]) => re.test(agent))?.[0];

export function appareil(agent) {
  const a = String(agent || '');
  const navigateur = trouver(NAVIGATEURS, a);
  const systeme = trouver(SYSTEMES, a);
  if (navigateur && systeme) return `${navigateur} sur ${systeme}`;
  return navigateur || systeme || 'Appareil inconnu';
}

export const dateCourte = (secondes) => new Date(secondes * 1000)
  .toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' });

export const ligneSession = (s) => `<li class="session" data-id="${esc(s.id)}">
  <span class="session-infos"><strong>${esc(appareil(s.agent))}</strong>${s.courante ? ' <em class="session-ici">cet appareil</em>' : ''}
  <small>Connecté le ${dateCourte(s.cree_le)}</small></span>
  ${s.courante ? '' : '<button type="button" class="bouton" data-revoquer>Révoquer</button>'}</li>`;
