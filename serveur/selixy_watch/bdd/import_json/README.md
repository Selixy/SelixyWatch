# bdd/import_json

Import unique des données JSON de production (`arbre.json`, `medias.json`, `profils.json`, `chat.json`) vers PostgreSQL.
Point d'entrée : `serveur/importer_json.py`.

## Procédure

1. Sauvegarder le dossier de données de production (copie complète, médias compris).
2. Simulation (aucune écriture, pas de connexion à la base) :
   `python importer_json.py --dossier DIR --proprietaire PSEUDO`
3. Lire le rapport : nombres par table, pseudos invalides, collisions, médias orphelins, fichiers manquants sur disque.
4. Résoudre chaque blocage avec `--renommer ancien=nouveau` (répétable), puis relancer la simulation jusqu'à « Aucun blocage ».
5. Appliquer : même commande plus `--appliquer --definir-mdp` (saisie masquée du mot de passe du propriétaire : sans lui, le premier venu
   qui se connecte sous ce pseudo hérité en fixerait le mot de passe). Le schéma est migré, puis tout s'écrit en une seule transaction.
   `BDD_URL` désigne la base visée.

## Décisions et pièges

- Tout le contenu (nœuds, médias) appartient au compte `--proprietaire` (pseudo de `profils.json`, avant ou après renommage).
  Les autres profils deviennent des comptes hérités (`mdp_hash` NULL) : id, avatar et version conservés.
- Aucun renommage silencieux : un pseudo invalide ou en collision (même squelette, donc `Intel`/`lntel` aussi) bloque l'application.
- Base non vide (comptes ou nœuds) : refus, transaction annulée. La simulation ne contacte pas la base et ne le détecte donc pas.
- Les ids sont conservés (adresses de room). Le rang d'un nœud est sa position parmi ses frères dans `arbre.json`.
- Médias jamais placés dans une playlist : ignorés et listés. Pistes vers un média absent de `medias.json` : ignorées et listées.
  Deux médias YouTube de même vidéo sont fusionnés sur le premier (contrainte d'unicité par propriétaire).
- Messages : `compte_id` seulement si l'auteur est un compte importé, sinon NULL ; le pseudo d'origine est conservé.
  Les canaux sans playlist correspondante sont comptés et ignorés. `canaux.json` n'est pas importé (état en mémoire).
- Les fichiers médias ne sont pas déplacés : l'import vérifie seulement leur présence dans `<dossier>/medias/`.
