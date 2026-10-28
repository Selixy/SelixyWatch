import os
import re

from fonctions import analyser_fonctions
from masquage import masquer
from vue import decouper_vue

RE_ANY = re.compile(r':\s*any\b|\bas\s+any\b|<any>|\bany\[\]|\bany\s*[,>)]')
ZONES_TYPEES = ()


def script_vue_non_type(texte, type_fichier):
    balises = re.findall(r'<script\b[^>]*>', texte)
    return type_fichier == 'vue' and any('lang="ts"' not in balise for balise in balises)


def mesurer_contenu(texte, type_fichier):
    if type_fichier == 'vue':
        script, gabarit, style, lignes = decouper_vue(texte)
        masque, commentaires = masquer(script, 'ts')
        commentaires += len(re.findall('<!--', gabarit)) + masquer(style, 'css')[1]
        return lignes, masque + '\n' + gabarit, masque, commentaires
    masque, commentaires = masquer(texte, type_fichier)
    return len(texte.splitlines()), masque, masque, commentaires


def calculer_ecarts(racine, chemin, type_fichier):
    with open(os.path.join(racine, chemin), encoding='utf-8', errors='replace') as flux:
        texte = flux.read()
    lignes, pour_any, pour_fonctions, commentaires = mesurer_contenu(texte, type_fichier)
    typage = chemin.startswith(ZONES_TYPEES)
    limite = 150 if type_fichier == 'vue' else 200
    fonctions = analyser_fonctions(pour_fonctions, 'ts' if type_fichier == 'vue' else type_fichier)
    longues = [f'{nom}={taille}>50' for nom, taille in fonctions if taille > 50]
    ecarts = {}
    if lignes > limite:
        ecarts['lignes'] = f'{lignes}>{limite}'
    if len(fonctions) > 5:
        ecarts['fonctions'] = f'{len(fonctions)}>5'
    if longues:
        ecarts['longueur'] = ','.join(longues)
    if commentaires:
        ecarts['commentaires'] = str(commentaires)
    if typage and type_fichier in ('ts', 'vue') and RE_ANY.search(pour_any):
        ecarts['any'] = str(len(RE_ANY.findall(pour_any)))
    if typage and (chemin.endswith(('.js', '.mjs', '.cjs')) or script_vue_non_type(texte, type_fichier)):
        ecarts['js'] = 'non-type'
    return ecarts
