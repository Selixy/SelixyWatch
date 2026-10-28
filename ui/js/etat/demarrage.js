import { etalonner } from './horloge.js';
import { connecter } from './flux.js';

export function demarrer(avecCanal = true) {
  etalonner();
  connecter(avecCanal);
}
