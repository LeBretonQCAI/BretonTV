# BretonTV playlist tooling

Ce dépôt contient désormais un petit utilitaire en ligne de commande pour explorer les fichiers M3U de BretonTV. L'objectif est de fournir un moyen rapide de filtrer, classer et inspecter les différentes chaînes listées dans les playlists.

## Installation

Aucune dépendance externe n'est nécessaire : l'outil repose exclusivement sur la bibliothèque standard de Python 3.10+.

## Utilisation

```bash
python -m bretontv BretonTV.m3u --country CA --limit 5
```

Options principales :

- `--country` : filtre par code pays (insensible à la casse).
- `--group` : limite aux chaînes d'un groupe (`group-title`).
- `--search` : applique un filtre texte sur le nom, l'identifiant ou l'URL.
- `--format json` : exporte les résultats au format JSON.
- `--list-groups` / `--list-countries` : affiche les valeurs disponibles puis quitte.

## Tests

```bash
python -m unittest
```
