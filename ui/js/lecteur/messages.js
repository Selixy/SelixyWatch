import { $ } from '../ui.js';

export const message = (t) => { $('#message').textContent = t || ''; };
export const erreur = (e) => message(e.message);
