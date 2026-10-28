export const lireLocal = (k, d) => { try { return localStorage.getItem(k) ?? d; } catch { return d; } };
export const ecrireLocal = (k, v) => { try { localStorage.setItem(k, v); } catch { return; } };
