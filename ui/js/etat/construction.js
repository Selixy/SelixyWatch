export function lireReponse(statut, donnees) {
  if (statut === 401) return { anonyme: true, noeuds: [], medias: {} };
  if (statut !== 200 || !donnees) return null;
  return { anonyme: false, noeuds: donnees.noeuds || [], medias: donnees.medias || {} };
}
