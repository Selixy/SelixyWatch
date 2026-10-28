import { icone } from '../ui.js';
import { peutModifier, peutRenommer, estProprietaire, estRacineRecue } from '../etat.js';

const mini = (action, titre, nomIcone, taille = 14, classe = '') =>
  `<button type="button" class="mini ${classe}" data-a="${action}" title="${titre}" aria-label="${titre}">${icone(nomIcone, taille)}</button>`;

export function boutonsLigne(n) {
  const b = [];
  if (n.type === 'playlist') b.push(mini('entrer', 'Entrer dans la room', 'entrer', 16, 'entrer'));
  if (estProprietaire(n)) b.push(mini('partager', 'Partager', 'inviter'));
  if (peutRenommer(n)) b.push(mini('renommer', 'Renommer (F2)', 'crayon'));
  if (estRacineRecue(n)) b.push(mini('quitter', 'Quitter ce partage', 'retirer', 14, 'danger'));
  else if (peutModifier(n)) b.push(mini('supprimer', 'Supprimer (Suppr)', 'poubelle', 14, 'danger'));
  return b.length ? `<span class="actions">${b.join('')}</span>` : '';
}
