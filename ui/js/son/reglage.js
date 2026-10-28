const CLE = 'mu-muet';

export const estMuet = () => { try { return localStorage.getItem(CLE) === '1'; } catch { return false; } };
export const fixerMuet = (b) => { try { localStorage.setItem(CLE, b ? '1' : '0'); } catch { return; } };
export const estCleMuet = (cle) => cle === CLE;
