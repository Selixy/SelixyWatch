export const lire = (cle, defaut) => { try { return localStorage.getItem(cle) ?? defaut; } catch { return defaut; } };
export const ecrire = (cle, valeur) => { try { localStorage.setItem(cle, valeur); } catch { return; } };
export const ouverts = new Set(JSON.parse(lire('mu-ouverts', '[]')));
export const sauverOuverts = () => ecrire('mu-ouverts', JSON.stringify([...ouverts]));
export const memoriserVue = (id) => ecrire('mu-playlist-vue', id || '');
