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

```text
.
├── Data/            # Modélisations document MongoDB (schemas, JSON examples)
├── Code/            # Scripts de conversion PostgreSQL → JSON → MongoDB
├── Interface_mission5.exe/             # Script Python pour ingestion automatique (pagila2..pagila5)
├── Reports/         # Rapport, explications et analyses
└── README.md        # Documentation générale du projet
