import { esc, icone, avatar } from '../ui.js';
import { formaterDate } from './lien.js';

export const htmlLien = (lien) => lien
  ? `<div class="partage-lien"><input type="text" readonly value="${esc(lien)}" aria-label="Lien d'invitation">` +
    '<button type="button" class="bouton" data-a="copier">Copier</button></div>'
  : '';

export const htmlContenu = (noeuds) => `<ul class="partage-liste">${(noeuds || []).map((n) =>
  `<li><span class="nom">${esc(n.nom)}</span><span class="note">${n.type === 'dossier' ? 'Dossier' : 'Playlist'}</span></li>`).join('')}</ul>`;

export const htmlInvites = (invites) => invites.length
  ? `<ul class="partage-liste">${invites.map((i) =>
    `<li><span class="partage-qui">${avatar(i.compte, 22)}<span class="nom">${esc(i.compte.pseudo)}</span></span>` +
    `<button type="button" class="mini danger" data-a="retirer" data-compte="${esc(i.compte.id)}" title="Retirer" aria-label="Retirer">${icone('retirer', 14)}</button></li>`).join('')}</ul>`
  : '<p class="note">Personne n\'a encore rejoint.</p>';

const couvre = (i) => (i.noeuds || []).map((n) => esc(n.nom)).join(', ') || 'Lien';

export const htmlInvitations = (invitations) => invitations.length
  ? `<ul class="partage-liste">${invitations.map((i) =>
    `<li><span class="nom">${couvre(i)} · ${i.usages}/${i.usages_max} utilisé${i.usages > 1 ? 's' : ''} · jusqu'au ${formaterDate(i.expire_le)}</span>` +
    `<button type="button" class="mini danger" data-a="revoquer" data-invitation="${esc(i.id)}" title="Révoquer" aria-label="Révoquer">${icone('retirer', 14)}</button></li>`).join('')}</ul>`
  : '<p class="note">Aucune invitation active.</p>';
