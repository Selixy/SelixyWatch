const BANDE_BASSE = 2;
const BANDE_HAUTE = 20;
const PLANCHER = 28;
const PLAFOND = 150;

let contexte = null;

export function contexteAudio() {
  contexte ??= new AudioContext();
  if (contexte.state === 'suspended') contexte.resume().catch(() => {});
  return contexte;
}

export function creerAnalyseur(piste) {
  const ctx = contexteAudio();
  const source = ctx.createMediaStreamSource(new MediaStream([piste]));
  const noeud = ctx.createAnalyser();
  noeud.fftSize = 256;
  noeud.smoothingTimeConstant = 0.6;
  source.connect(noeud);
  return { source, noeud, spectre: new Uint8Array(noeud.frequencyBinCount) };
}

export function mesurerNiveau(analyseur) {
  analyseur.noeud.getByteFrequencyData(analyseur.spectre);
  let somme = 0;
  for (let i = BANDE_BASSE; i < BANDE_HAUTE; i++) somme += analyseur.spectre[i];
  const moyenne = somme / (BANDE_HAUTE - BANDE_BASSE);
  return Math.max(0, Math.min(1, (moyenne - PLANCHER) / (PLAFOND - PLANCHER)));
}

export function libererAnalyseur(analyseur) {
  analyseur.source.disconnect();
  analyseur.noeud.disconnect();
}
