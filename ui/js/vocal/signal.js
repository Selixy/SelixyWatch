import { S, action } from '../etat.js';

export async function signaler(act, data = null, cible = null) {
  if (!S.canal) return;
  try {
    await action(S.canal, 'signal', { action: act, data, cible });
  } catch (e) {
    console.warn('Erreur signal vocal:', e);
  }
}
