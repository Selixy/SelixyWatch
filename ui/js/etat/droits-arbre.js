import { peutModifier } from './droits.js';

export function deplacementPermis(n, vers, noeud) {
  if (!n) return false;
  return vers === 'racine' || noeud(vers)?.type === 'dossier';
}

export function parentDeCreation(selection, noeud) {
  const n = noeud(selection);
  const cible = n?.type === 'dossier' ? n : noeud(n?.parent);
  return peutModifier(cible) ? cible.id : 'racine';
}
