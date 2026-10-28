import { brancherElement } from './capture.js';

export function creerReference(ctx, lecteurs) {
  const noeud = ctx.createGain();
  const liberations = [...lecteurs].map((el) => brancherElement(ctx, el, noeud));
  return {
    noeud,
    liberer() {
      for (const liberer of liberations) liberer();
      noeud.disconnect();
    }
  };
}
