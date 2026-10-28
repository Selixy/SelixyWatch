import { contexteAudio } from '../voix-analyse.js';
import { creerReference } from './reference.js';

let module = null;

function chargerModule(ctx) {
  module ??= ctx.audioWorklet.addModule(new URL('./processeur.js', import.meta.url));
  return module;
}

function construire(ctx, brute, lecteurs) {
  const source = ctx.createMediaStreamSource(new MediaStream([brute]));
  const reference = creerReference(ctx, lecteurs);
  const noeud = new AudioWorkletNode(ctx, 'annuleur-echo', {
    numberOfInputs: 2,
    numberOfOutputs: 1,
    outputChannelCount: [1],
    channelCount: 1,
    channelCountMode: 'explicit'
  });
  const destination = ctx.createMediaStreamDestination();
  source.connect(noeud, 0, 0);
  reference.noeud.connect(noeud, 0, 1);
  noeud.connect(destination);
  const liberer = () => {
    source.disconnect();
    noeud.disconnect();
    reference.liberer();
  };
  return { piste: destination.stream.getAudioTracks()[0], liberer };
}

export async function filtrerMicro(brute, lecteurs) {
  try {
    const ctx = contexteAudio();
    await chargerModule(ctx);
    const { piste, liberer } = construire(ctx, brute, lecteurs);
    const arreter = piste.stop.bind(piste);
    piste.stop = () => {
      arreter();
      brute.stop();
      liberer();
    };
    return piste;
  } catch (e) {
    return brute;
  }
}
