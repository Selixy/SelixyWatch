import { $ } from '../ui.js';
import { etat } from '../etat.js';
import { L, elements, courant } from './contexte.js';

export function repos() {
  const { ecran, salle } = elements;
  const c = $('#commandes');
  const focusClavier = c.contains(document.activeElement) && document.activeElement.matches(':focus-visible');
  const pleinAvecChat = salle.classList.contains('plein') && salle.classList.contains('chat-ouvert');
  const fige = L.doigtPose || !etat()?.lecture || !courant() || c.matches(':hover') || focusClavier || pleinAvecChat;
  if (!courant()) L.masqueesParToucher = false;
  ecran.classList.toggle('repos', L.masqueesParToucher || (!fige && Date.now() - L.dernierGeste > 2500));
}

export function reveiller() {
  const { ecran } = elements;
  if (ecran.classList.contains('repos')) L.revelee = Date.now();
  L.dernierGeste = Date.now();
  ecran.classList.remove('repos');
}
