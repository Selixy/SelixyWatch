import { $ } from './ui.js';
import { initCompte } from './compte.js';
import { saisie } from './login/saisie.js';
import { apercu } from './login/affichage.js';
import { brancherChoixAvatar } from './login/choix-avatar.js';
import { soumettre } from './login/envoi.js';
import { soumettreAuth } from './login/authentification.js';
import { brancherModes } from './login/mode.js';
import { brancherAnonyme } from './login/anonyme.js';
import { brancherOubli } from './login/oubli.js';
import { montrerProfil } from './login/profil.js';

brancherChoixAvatar();
brancherModes();
brancherAnonyme();
brancherOubli();
$('#profil').onsubmit = soumettre;
$('#auth').onsubmit = soumettreAuth;

saisie.profil = await initCompte();
if (saisie.profil) montrerProfil(saisie.profil);
else $('#auth').hidden = false;
apercu();
