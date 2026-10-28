const UNITES = ['o', 'Ko', 'Mo', 'Go', 'To'];

export function formaterOctets(n) {
  let v = Math.max(0, Number(n) || 0);
  let u = 0;
  while (v >= 1024 && u < UNITES.length - 1) { v /= 1024; u += 1; }
  const texte = u === 0 || v >= 10 ? String(Math.round(v)) : v.toFixed(1).replace('.', ',');
  return `${texte} ${UNITES[u]}`;
}

export const pourcentage = (utilise, quota) => (quota > 0 ? Math.min(100, Math.round((utilise / quota) * 100)) : 0);

export const illimite = (profil) => profil?.quota === null;

export const texteQuota = (profil) => (illimite(profil)
  ? `${formaterOctets(profil.utilise)} utilisés · illimité`
  : `${formaterOctets(profil.utilise)} utilisés sur ${formaterOctets(profil.quota)}`);

export function afficherQuota(profil, racine = document) {
  const bloc = racine.querySelector('#quota');
  if (!bloc || !(illimite(profil) || profil?.quota > 0)) return;
  racine.querySelector('#quota-texte').textContent = texteQuota(profil);
  racine.querySelector('#quota-barre').style.width = illimite(profil) ? '0%' : pourcentage(profil.utilise, profil.quota) + '%';
  bloc.hidden = false;
}
