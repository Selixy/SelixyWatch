export function lireBoites(octets) {
  const vue = new DataView(octets.buffer, octets.byteOffset, octets.byteLength);
  const boites = [];
  let i = 0;
  while (i + 8 <= octets.length) {
    let taille = vue.getUint32(i);
    if (taille === 1 && i + 16 <= octets.length) taille = Number(vue.getBigUint64(i + 8));
    if (taille < 8) break;
    boites.push({ type: String.fromCharCode(...octets.subarray(i + 4, i + 8)), debut: i, taille });
    i += taille;
  }
  return boites;
}

export function lireSidx(octets, boite) {
  const v = new DataView(octets.buffer, octets.byteOffset + boite.debut, boite.taille);
  const large = v.getUint8(8) === 1;
  const echelle = v.getUint32(16);
  const lire = (p) => (large ? Number(v.getBigUint64(p)) : v.getUint32(p));
  const pas = large ? 8 : 4;
  let temps = lire(20);
  let octet = boite.debut + boite.taille + lire(20 + pas);
  const reference = 20 + 2 * pas + 2;
  const segments = [];
  for (let i = 0, p = reference + 2; i < v.getUint16(reference); i++, p += 12) {
    const taille = v.getUint32(p) & 0x7fffffff;
    const duree = v.getUint32(p + 4);
    segments.push({ debut: temps / echelle, fin: (temps + duree) / echelle, octet, taille });
    octet += taille;
    temps += duree;
  }
  return segments;
}
