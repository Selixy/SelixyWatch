export async function lireOctets(adresse, debut, fin) {
  const reponse = await fetch(adresse, { headers: { Range: `bytes=${debut}-${fin}` } });
  if (!reponse.ok) throw new Error(`flux ${reponse.status}`);
  return new Uint8Array(await reponse.arrayBuffer());
}

export async function lireInformations(id) {
  const reponse = await fetch(`/flux/${id}/info`);
  if (!reponse.ok) throw new Error(`flux ${reponse.status}`);
  return reponse.json();
}
