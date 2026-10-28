import { lireBoites, lireSidx } from './mp4.js';

const TAILLES_ESSAI = [65536, 1048576];

export async function lireIndex(adresse, lireOctets) {
  for (const taille of TAILLES_ESSAI) {
    const octets = await lireOctets(adresse, 0, taille - 1);
    const sidx = lireBoites(octets).find((b) => b.type === 'sidx');
    if (sidx && sidx.debut + sidx.taille <= octets.length) {
      return { init: octets.slice(0, sidx.debut), segments: lireSidx(octets, sidx) };
    }
  }
  throw new Error('index du flux introuvable');
}
