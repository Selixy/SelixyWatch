import test from 'node:test';
import assert from 'node:assert/strict';
import { creerAnnuleur } from '../../ui/js/vocal/echo/annuleur.js';

const TAUX = 16000;
const RETARD = 1920;
const CHEMIN = [0.5, 0.3, -0.2, 0.1, 0.05];

function alea(graine) {
  let etat = graine;
  return () => {
    etat = (etat * 1664525 + 1013904223) % 4294967296;
    return etat / 2147483648 - 1;
  };
}

function scene(secondes, avecVoix) {
  const tirer = alea(7);
  const total = secondes * TAUX;
  const ref = new Float32Array(total);
  const voix = new Float32Array(total);
  let enveloppe = 0.3;
  let passe = 0;
  for (let i = 0; i < total; i++) {
    if (i % 1600 === 0) enveloppe = 0.1 + Math.abs(tirer()) * 0.5;
    passe = passe * 0.6 + tirer() * enveloppe * 0.4;
    ref[i] = passe;
    if (avecVoix && i > total * 0.7) voix[i] = 0.25 * Math.sin(i * 0.11) * Math.sin(i * 0.0007);
  }
  const mic = new Float32Array(total);
  for (let i = 0; i < total; i++) {
    let echo = 0;
    for (let k = 0; k < CHEMIN.length; k++) echo += CHEMIN[k] * (ref[i - RETARD - k] ?? 0);
    mic[i] = echo + voix[i] + tirer() * 0.001;
  }
  return { ref, mic, voix };
}

const energie = (serie, de, a) => serie.slice(de, a).reduce((s, v) => s + v * v, 0);

function passer({ ref, mic }) {
  const annuleur = creerAnnuleur(TAUX);
  return mic.map((m, i) => annuleur.traiter(m, ref[i]));
}

test('l\'écho du lecteur est atténué d\'au moins 15 dB une fois le filtre convergé', () => {
  const donnees = scene(10, false);
  const sortie = passer(donnees);
  const de = 6 * TAUX, a = 10 * TAUX;
  const gain = 10 * Math.log10(energie(donnees.mic, de, a) / energie(sortie, de, a));
  assert.ok(gain > 15, `atténuation ${gain.toFixed(1)} dB`);
});

test('la voix qui parle par-dessus le lecteur est conservée', () => {
  const donnees = scene(10, true);
  const sortie = passer(donnees);
  const de = Math.floor(8 * TAUX), a = 10 * TAUX;
  const rapport = energie(sortie, de, a) / energie(donnees.voix, de, a);
  assert.ok(rapport > 0.4 && rapport < 2, `rapport d'énergie ${rapport.toFixed(2)}`);
});

test('sans lecteur, le micro passe tel quel', () => {
  const donnees = scene(2, true);
  const silence = new Float32Array(donnees.ref.length);
  const sortie = passer({ ref: silence, mic: donnees.voix });
  const rapport = energie(sortie, 0, sortie.length) / energie(donnees.voix, 0, sortie.length);
  assert.ok(rapport > 0.95 && rapport < 1.05, `rapport ${rapport.toFixed(3)}`);
});
