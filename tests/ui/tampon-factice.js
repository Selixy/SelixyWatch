import { TAILLE_SEGMENT } from './mp4-factice.js';

export class TamponFactice extends EventTarget {
  constructor() {
    super();
    this.plages = [];
    this.ajouts = [];
  }

  get buffered() {
    const plages = this.plages;
    return { length: plages.length, start: (i) => plages[i][0], end: (i) => plages[i][1] };
  }

  appendBuffer(octets) {
    const segment = octets.length === TAILLE_SEGMENT;
    this.ajouts.push(segment ? octets[0] : 'init');
    if (segment) this.plages = fusionner([...this.plages, [octets[0] * 5, octets[0] * 5 + 5]]);
    queueMicrotask(() => this.dispatchEvent(new Event('updateend')));
  }

  remove(debut, fin) {
    this.plages = this.plages.map(([a, b]) => [Math.max(a, fin), b]).filter(([a, b]) => a < b);
    queueMicrotask(() => this.dispatchEvent(new Event('updateend')));
  }
}

export function fusionner(plages) {
  const triees = [...plages].sort((a, b) => a[0] - b[0]);
  return triees.reduce((acc, [a, b]) => {
    const dernier = acc[acc.length - 1];
    if (dernier && a <= dernier[1] + 0.01) dernier[1] = Math.max(dernier[1], b);
    else acc.push([a, b]);
    return acc;
  }, []);
}
