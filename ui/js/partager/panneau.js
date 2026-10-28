import { $ } from '../ui.js';
import { noeud } from '../etat.js';
import { lirePartage, actionPartage } from './requetes.js';
import { htmlInvites, htmlInvitations } from './rendu.js';
import { ouvrirFenetre, fermer } from './fenetre.js';
import { ouvrirInviter } from './inviter.js';

const ACTIONS = {
  retirer: (id, el) => actionPartage(id, 'retirer', { compte: el.dataset.compte }),
  revoquer: (id, el) => actionPartage(id, 'revoquer', { invitation: el.dataset.invitation }),
};

const CORPS = '<button type="button" class="bouton principal" data-a="inviter">Créer un lien d\'invitation</button>' +
  '<h3>Invités</h3><div id="partage-invites"></div><h3>Invitations actives</h3><div id="partage-invitations"></div>';

let voile = null;
const dire = (texte) => { $('.message', voile).textContent = texte || ''; };

async function actualiser(id) {
  try {
    const p = await lirePartage(id);
    $('#partage-invites', voile).innerHTML = htmlInvites(p.invites || []);
    $('#partage-invitations', voile).innerHTML = htmlInvitations(p.invitations || []);
  } catch (e) { dire(e.message); }
}

async function agir(id, faire) {
  try { await faire(); dire(''); } catch (e) { dire(e.message); }
  await actualiser(id);
}

export async function ouvrirPartage(id) {
  voile = ouvrirFenetre(`Partager « ${noeud(id)?.nom ?? ''} »`, CORPS);
  voile.addEventListener('click', (e) => {
    const b = e.target.closest('[data-a]');
    if (e.target === voile || b?.dataset.a === 'fermer') return fermer();
    if (b?.dataset.a === 'inviter') ouvrirInviter(id);
    else if (b && ACTIONS[b.dataset.a]) agir(id, () => ACTIONS[b.dataset.a](id, b));
  });
  await actualiser(id);
}
