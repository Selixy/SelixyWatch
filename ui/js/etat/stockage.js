export const lire = (cle, defaut) => { try { return localStorage.getItem(cle) ?? defaut; } catch { return defaut; } };
export const ecrire = (cle, valeur) => { try { localStorage.setItem(cle, valeur); } catch { return; } };
export const effacer = (cle) => { try { localStorage.removeItem(cle); } catch { return; } };
