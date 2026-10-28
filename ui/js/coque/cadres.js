export const cadre = (v) => document.querySelector(`iframe[data-vue="${v}"]`);
export const cadres = () => document.querySelectorAll('iframe[data-vue]');
export const canalMemorise = () => { try { return localStorage.getItem('mu-canal'); } catch { return null; } };
