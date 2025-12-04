# Pagila-Mongo-Migrator

![Status](https://img.shields.io/badge/Status-Terminer-orange)
![Database](https://img.shields.io/badge/Database-PostgreSQL_→_MongoDB-blue)
![Python](https://img.shields.io/badge/Python-Scripts_ETL-yellow)
![GUI](https://img.shields.io/badge/Interface-Graphique-green)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

Projet réalisé dans le cadre de la SAÉ portant sur la **migration de données d’un modèle relationnel PostgreSQL vers une base NoSQL MongoDB**.  
Le travail consiste à modéliser, convertir et automatiser l’ingestion de données au format JSON, tout en fournissant une **interface graphique** pour la saisie et l’insertion de documents.

---

## 🎯 Objectifs du projet

- Créer plusieurs bases PostgreSQL (`pagila1` … `pagila5`) à partir d’un schéma commun **FILM / ACTOR / FILM_ACTOR**.  
- Identifier et proposer des **modélisations orientées document** adaptées à MongoDB.  
- Convertir la base `pagila1` en JSON puis l’importer dans MongoDB :  
  - via PostgreSQL  
  - via Python  
- Développer un **script Python d’ETL automatisé** permettant d’importer les bases pagila2 → pagila5 et les futures bases similaires.  
- Concevoir une **interface graphique Python** permettant à un utilisateur de saisir un document (selon le modèle choisi) et de l’insérer automatiquement dans MongoDB.

---

## 🗂 Organisation du dépôt
🧱 Structure relationnelle de départ (PostgreSQL)

Les bases pagila1…pagila5 sont créées à partir du schéma suivant :
(extrait du sujet officiel) 

FILM
Attribut	Description
film_id	identifiant du film
title	titre
description	résumé
language_id	langue principale
original_language_id	langue originale
ACTOR
Attribut	Description
actor_id	identifiant
first_name	prénom
last_name	nom
FILM_ACTOR

Relation n-n entre films et acteurs.

🗃️ Modélisation orientée document (MongoDB)

Exemples de modèles possibles :

Modèle 1 – Film centré :
{
  "film_id": 1,
  "title": "Example",
  "description": "Résumé...",
  "actors": [
    { "actor_id": 10, "first_name": "John", "last_name": "Doe" }
  ],
  "language": { "id": 1, "name": "English" }
}

Modèle 2 – Acteur centré :
{
  "actor_id": 10,
  "name": "John Doe",
  "films": [
    { "film_id": 1, "title": "Example" }
  ]
}

⚙️ Flux de conversion et migration (pipeline)

Export PostgreSQL → JSON

Nettoyage, structuration et transformation des documents

Injection dans MongoDB

via commandes Mongo

via script Python

Automatisation (ETL Python)

Parcours de pagila2 → pagila5

Détection automatique de nouvelles bases

Conversion + insertion en masse

🖥️ Interface Graphique (GUI)

Création d’un nouveau document film / acteur

Génération automatique du JSON valide

Insertion directe dans MongoDB

Vérification et affichage de confirmation

🛠 Technologies utilisées

PostgreSQL

MongoDB

Python (pymongo, psycopg2, tkinter, json)

Commandes Mongo / Postgres

JSON normalisé

📄 Livrables

Modélisations document

Scripts SQL

Scripts Python (conversion, ETL, GUI)

Base MongoDB finale

Rapport
