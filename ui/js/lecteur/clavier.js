import { icone } from '../ui.js';
import { etat, agir } from '../etat.js';
import { L, courant, longueur } from './contexte.js';
import { bascule, aller, deplacer } from './actions.js';
import { erreur } from './messages.js';
import { indiquer } from './indicateur.js';
import { reveiller } from './repos.js';
import { volume, muet } from './reglages-son.js';
import { plein } from './salle-etat.js';
import { majPlein, pleinEcran } from './plein.js';
import { chatPlein } from './chat-plein.js';
import { cinema } from './cinema.js';

function touche(ev) {
  if (ev.ctrlKey || ev.altKey || ev.metaKey) return;
  const t = ev.target;
  if (t.closest?.('input, textarea, select, [contenteditable]') && !(t.id === 'volume')) return;
  const k = ev.key, m = courant();
  const fait = (f) => { ev.preventDefault(); reveiller(); f(); };
  if (k === ' ' || k === 'Spacebar' || ev.code === 'Space') {
    return fait(() => { bascule(); indiquer(icone(etat()?.lecture ? 'pause' : 'play', 40)); });
  }
  if (k === 'Escape' && plein() && !document.fullscreenElement) return fait(() => majPlein(false));
  if ((k === 'c' || k === 'C') && !ev.shiftKey && plein()) return fait(() => chatPlein());
  if (ev.shiftKey && (k === 'N' || k === 'n')) return fait(() => { if (m) agir('suivant').catch(erreur); indiquer(icone('next', 40)); });
  if (ev.shiftKey && (k === 'P' || k === 'p')) return fait(() => { if (m) agir('precedent').catch(erreur); indiquer(icone('prev', 40)); });
  if (ev.shiftKey) return;
  switch (k) {
    case 'k': case 'K':
      return fait(() => { bascule(); indiquer(icone(etat()?.lecture ? 'pause' : 'play', 40)); });
    case 'j': case 'J': return fait(() => deplacer(-10));
    case 'l': case 'L': return fait(() => deplacer(10));
    case 'ArrowLeft': return fait(() => deplacer(-5));
    case 'ArrowRight': return fait(() => deplacer(5));
    case 'ArrowUp': return fait(() => { volume((L.mut ? 0 : L.vol) + 0.05); indiquer(`${Math.round(L.vol * 100)} %`); });
    case 'ArrowDown': return fait(() => { volume((L.mut ? 0 : L.vol) - 0.05); indiquer(`${Math.round(L.vol * 100)} %`); });
    case 'm': case 'M': return fait(() => { muet(); indiquer(icone(L.mut ? 'muet' : 'volume', 40)); });
    case 'f': case 'F': return fait(pleinEcran);
    case 't': case 'T': return fait(() => cinema());
    case 'Home': return fait(() => { aller(0); indiquer('0:00'); });
    case 'End': return fait(() => { const d = longueur(); aller(Math.max(0, d - 0.5)); indiquer(icone('next', 40)); });
    default:
      if (/^[0-9]$/.test(k)) return fait(() => { aller((longueur() * Number(k)) / 10); indiquer(`${Number(k) * 10} %`); });
  }
}

export const initClavier = () => document.addEventListener('keydown', touche);
