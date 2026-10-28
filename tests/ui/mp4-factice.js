export const TAILLE_SEGMENT = 100;
export const DUREE_SEGMENT = 5;

function boite(type, charge) {
  const octets = new Uint8Array(8 + charge.length);
  new DataView(octets.buffer).setUint32(0, octets.length);
  octets.set([...type].map((c) => c.charCodeAt(0)), 4);
  octets.set(charge, 8);
  return octets;
}

export function construireEntete(nombre) {
  const charge = new Uint8Array(12 + 8 + 4 + 12 * nombre);
  const vue = new DataView(charge.buffer);
  vue.setUint32(8, 1000);
  vue.setUint16(22, nombre);
  for (let i = 0; i < nombre; i++) {
    vue.setUint32(24 + 12 * i, TAILLE_SEGMENT);
    vue.setUint32(28 + 12 * i, DUREE_SEGMENT * 1000);
  }
  const entete = [boite('ftyp', new Uint8Array(8)), boite('moov', new Uint8Array(20)), boite('sidx', charge)];
  const octets = new Uint8Array(entete.reduce((somme, b) => somme + b.length, 0));
  entete.reduce((debut, b) => { octets.set(b, debut); return debut + b.length; }, 0);
  return octets;
}
