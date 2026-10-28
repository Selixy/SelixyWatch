import { CHEMINS, PLEINS } from './trace-icones.js';

export const icone = (nom, taille = 16) =>
  `<svg viewBox="0 0 24 24" width="${taille}" height="${taille}" aria-hidden="true" focusable="false" ` +
  `fill="${PLEINS.has(nom) ? 'currentColor' : 'none'}" stroke="${PLEINS.has(nom) ? 'none' : 'currentColor'}" ` +
  `stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="${CHEMINS[nom]}"/></svg>`;
