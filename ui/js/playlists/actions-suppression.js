import { noeud, enfants, actionArbre, estRacineRecue, peutModifier } from '../etat.js';
import { quitter } from '../partager.js';
import { essayer, message } from './page.js';

export async function quitterPartage(id) {
  const n = noeud(id);
  if (n && confirm(`Quitter le partage « ${n.nom} » ? Vous n'y aurez plus accès sans nouvelle invitation.`)) await essayer(() => quitter(id));
}

export async function supprimer(id) {
  const n = noeud(id);
  if (!peutModifier(n)) return message('Vous ne pouvez pas modifier cet élément.');
  if (estRacineRecue(n)) return quitterPartage(id);
  const texte = n.type === 'dossier'
    ? `Supprimer le dossier « ${n.nom} »${enfants(id).length ? ' et tout son contenu' : ''} pour tout le monde ?`
    : `Supprimer la playlist « ${n.nom} » pour tout le monde ?`;
  if (confirm(texte)) await essayer(() => actionArbre('supprimer', { id }));
}
