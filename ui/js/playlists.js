import { $, icone } from './ui.js';
import { surChangement, demarrer } from './etat.js';
import { initCompte } from './compte.js';
import { definirRendu, P } from './playlists/page.js';
import { ouvrirInviter } from './partager.js';
import { rendrePage } from './playlists/rendu.js';
import { nouveau } from './playlists/actions-arbre.js';
import { brancherArbre } from './playlists/arbre-evenements.js';
import { brancherGlisserArbre } from './playlists/glisser-arbre.js';
import { brancherGlisserPistes } from './playlists/glisser-pistes.js';
import { brancherRetrait } from './playlists/actions-pistes.js';
import { brancherRecherche } from './playlists/recherche.js';
import { brancherCollage, erreursImport } from './playlists/liens.js';
import { brancherEnvoi } from './playlists/envoi.js';
import { appliquerDroitEnvoi } from './playlists/droit-envoi.js';
import { brancherOuverture } from './playlists/ouverture.js';

export { rendre } from './playlists/page.js';

definirRendu(rendrePage);
brancherRecherche();
brancherArbre();
brancherGlisserArbre();
brancherRetrait();
brancherGlisserPistes();
brancherCollage();
brancherEnvoi();
brancherOuverture(rendrePage);

for (const el of document.querySelectorAll('[data-icone]')) el.insertAdjacentHTML('afterbegin', icone(el.dataset.icone, 18));
$('#nouveau-dossier').onclick = () => nouveau('dossier');
$('#nouvelle-playlist').onclick = () => nouveau('playlist');
$('#inviter').onclick = () => ouvrirInviter(P.selection);

surChangement((quoi) => {
  if (quoi === 'import') erreursImport();
  rendrePage();
});
initCompte().then(appliquerDroitEnvoi);
demarrer(false);
