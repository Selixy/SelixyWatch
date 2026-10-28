export const lienComplet = (origine, lien) => origine + lien;

export function formaterDate(valeur) {
  const date = typeof valeur === 'number' ? new Date(valeur < 1e11 ? valeur * 1000 : valeur) : new Date(valeur);
  return Number.isNaN(date.getTime()) ? '' : date.toLocaleDateString('fr-FR', { day: 'numeric', month: 'short' });
}

export async function copier(texte) {
  try {
    await navigator.clipboard.writeText(texte);
    return true;
  } catch {
    return false;
  }
}
