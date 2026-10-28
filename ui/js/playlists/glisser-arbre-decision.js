import { noeud, enfants, estPlaylist, peutModifier, deplacementPermis } from '../etat.js';
import { P } from './page.js';

export const estDescendant = (id, ancetre) => { for (let n = noeud(id); n; n = noeud(n.parent)) if (n.id === ancetre) return true; return false; };

export function destination(e) {
  const l = e.target.closest('.ligne');
  if (!l) return { vers: 'racine', avant: null, zone: 'fond', ligne: null };
  const id = l.dataset.id, n = noeud(id), dossier = n.type === 'dossier';
  const r = l.getBoundingClientRect(), y = (e.clientY - r.top) / r.height;
  if (dossier && y >= 0.25 && y <= 0.75) return { vers: id, avant: null, zone: 'dans', ligne: l };
  if (y < (dossier ? 0.25 : 0.5)) return { vers: n.parent, avant: id, zone: 'avant', ligne: l };
  const freres = enfants(n.parent).filter((x) => x.id !== P.glisse);
  const suivant = freres[freres.findIndex((x) => x.id === id) + 1];
  return { vers: n.parent, avant: suivant ? suivant.id : null, zone: 'apres', ligne: l };
}

export const valide = (d) => P.glisse && d.vers !== P.glisse && !estDescendant(d.vers, P.glisse) && d.avant !== P.glisse &&
  deplacementPermis(noeud(P.glisse), d.vers, noeud);

export const playlistVisee = (e) => {
  const id = e.target.closest('.ligne')?.dataset.id;
  return estPlaylist(id) && peutModifier(noeud(id)) ? id : null;
};
