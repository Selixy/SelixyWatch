function capturer(el) {
  return el.captureStream?.() ?? el.mozCaptureStream?.() ?? null;
}

export function brancherElement(ctx, el, sortie) {
  const volume = ctx.createGain();
  volume.connect(sortie);
  const etat = { piste: null, source: null };
  const regler = () => { volume.gain.value = el.muted ? 0 : el.volume; };
  const rebrancher = () => {
    const piste = capturer(el)?.getAudioTracks()[0];
    if (!piste || piste === etat.piste) return;
    etat.source?.disconnect();
    etat.piste = piste;
    etat.source = ctx.createMediaStreamSource(new MediaStream([piste]));
    etat.source.connect(volume);
  };
  regler();
  rebrancher();
  el.addEventListener('volumechange', regler);
  for (const nom of ['loadedmetadata', 'playing']) el.addEventListener(nom, rebrancher);
  return () => {
    for (const nom of ['loadedmetadata', 'playing']) el.removeEventListener(nom, rebrancher);
    el.removeEventListener('volumechange', regler);
    etat.source?.disconnect();
    volume.disconnect();
  };
}
