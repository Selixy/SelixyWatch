const CAMERA_MAX = 240;
const CAMERA_MIN = 48;
const MARGE_BASSE = 28;
const MARGE_MOUVEMENT = 14;
const PART_AVATAR = 0.3;

export function meilleureTaille(nombre, largeur, hauteur, ecart) {
  let meilleure = 0;
  for (let colonnes = 1; colonnes <= nombre; colonnes++) {
    const lignes = Math.ceil(nombre / colonnes);
    const enLargeur = (largeur - (colonnes - 1) * ecart) / colonnes;
    const enHauteur = (hauteur - (lignes - 1) * ecart) / lignes;
    meilleure = Math.max(meilleure, Math.min(enLargeur, enHauteur));
  }
  return meilleure;
}

function espaceUtile(zone) {
  const style = getComputedStyle(zone);
  const [gauche, droite, haut, bas] = ['Left', 'Right', 'Top', 'Bottom'].map((c) => parseFloat(style[`padding${c}`]) || 0);
  const dessus = zone.getBoundingClientRect().top;
  const hauteur = window.innerHeight - dessus - MARGE_BASSE - haut - bas;
  const largeur = (zone.clientWidth || zone.parentElement?.clientWidth || 300) - gauche - droite;
  return {
    largeur: largeur - MARGE_MOUVEMENT,
    hauteur: hauteur - MARGE_MOUVEMENT,
    ecart: parseFloat(style.columnGap) || 16
  };
}

export function ajusterTaillesPresents() {
  const zone = document.getElementById('presents');
  if (!zone || zone.hidden) return;
  const nbVideos = zone.querySelectorAll('.present.avec-video').length;
  const nbAvatars = zone.querySelectorAll('.present:not(.avec-video)').length;
  if (nbVideos > 0) {
    const { largeur, hauteur, ecart } = espaceUtile(zone);
    const nombre = nbVideos + Math.ceil(nbAvatars * PART_AVATAR);
    const camera = Math.max(CAMERA_MIN, Math.min(CAMERA_MAX, meilleureTaille(nombre, largeur, hauteur, ecart)));
    zone.style.setProperty('--cam-taille', `${Math.round(camera)}px`);
    zone.style.setProperty('--p-taille', `${Math.max(26, Math.min(46, Math.round(camera * 0.28)))}px`);
  } else {
    const taille = Math.max(28, Math.min(48, Math.round(50 - Math.sqrt(nbAvatars) * 4.5)));
    zone.style.setProperty('--p-taille', `${taille}px`);
  }
}
