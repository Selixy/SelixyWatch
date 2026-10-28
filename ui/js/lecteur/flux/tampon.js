import { attendre } from './attente.js';

export const ajouter = (tampon, octets) => attendre(tampon, () => tampon.appendBuffer(octets));

export const retirer = (tampon, debut, fin) => attendre(tampon, () => tampon.remove(debut, fin));
