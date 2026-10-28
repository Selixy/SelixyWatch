import { demarrerFlux } from './session.js';

export function creerOrigineFlux(video) {
  let courant = null;
  return {
    url(id) {
      if (courant?.id !== id) {
        courant?.session.arreter();
        courant = { id, session: demarrerFlux(video, id) };
      }
      return courant.session.url;
    },
    arreter() {
      courant?.session.arreter();
      courant = null;
    },
  };
}
