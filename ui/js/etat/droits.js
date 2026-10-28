export const peutModifier = (n) => !!n && (n.role === 'editeur' || n.role === 'proprietaire');
export const estProprietaire = (n) => !!n && n.role === 'proprietaire';
export const estRacineRecue = (n) => !!n && n.partage_racine === true;
export const peutDeplacer = (n) => !!n;
export const peutRenommer = (n) => !!n;
