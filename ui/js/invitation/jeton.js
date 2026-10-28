export const CLE = 'invitation_en_attente';

export function lireJeton(hash) {
  const jeton = String(hash || '').replace(/^#/, '').trim();
  return /^[A-Za-z0-9_-]{8,200}$/.test(jeton) ? jeton : null;
}

export function garder(stockage, jeton) {
  try { stockage.setItem(CLE, jeton); } catch { return; }
}

export function enAttente(stockage) {
  try { return lireJeton(stockage.getItem(CLE)); } catch { return null; }
}

export function effacer(stockage) {
  try { stockage.removeItem(CLE); } catch { return; }
}
