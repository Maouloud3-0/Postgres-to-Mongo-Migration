# =============================================================================
# # ajout automatique dans pagila_
# =============================================================================
# =============================================================================
import psycopg2
from pymongo import MongoClient

def extract_and_load(database_name):
    try:
        # Connexion à PostgreSQL
        pg_conn = psycopg2.connect(database=database_name, user="postgres", password="Gaoussou2002", host="localhost")
        pg_cursor = pg_conn.cursor()

        # Exécution de la requête pour obtenir les données en format JSON
        pg_cursor.execute("""
            SELECT json_agg(row_to_json(t))
            FROM (
                SELECT film_id, title, description, language_id, original_language_id,
                    (
                        SELECT json_agg(row_to_json(a))
                        FROM (
                            SELECT actor.actor_id, actor.first_name, actor.last_name
                            FROM actor
                            INNER JOIN film_actor ON actor.actor_id = film_actor.actor_id
                            WHERE film_actor.film_id = film.film_id
                        ) a
                    ) as actors
                FROM film
            ) t;
        """)
        rows = pg_cursor.fetchone()[0]  # Prendre le premier résultat qui devrait être une liste JSON

        # Vérifier que rows n'est pas None et insérer dans MongoDB
        if rows:
            collection.insert_many(rows)
        else:
            print(f"Aucune donnée à importer de {database_name}.")

    except Exception as e:
        print(f"Une erreur s'est produite avec la base de données {database_name}: {e}")
    finally:
        if pg_cursor:
            pg_cursor.close()
        if pg_conn:
            pg_conn.close()

# Connexion à MongoDB
client = MongoClient('localhost', 27017)
db = client['Pagila_db']
collection = db['Pagila_']

# Itération sur les bases de données Pagila et insertion dans la même collection MongoDB
for i in range(2, 6):  # pour pagila2 à pagila5
    database_name = f"pagila{i}"
    extract_and_load(database_name)

# Fermeture de la connexion MongoDB
client.close()
print("Importation terminée pour toutes les bases de données.")

# =============================================================================
# =============================================================================
from pymongo import MongoClient
# Connexion à MongoDB
client = MongoClient('localhost', 27017)
db = client['Pagila_db']
collection = db['Pagila_']

# Affichage des documents de la collection films
for document in collection.find():
    print(document)

# Fermeture de la connexion
client.close()


# =============================================================================
# la version demande par madame 
# =============================================================================
import psycopg2
import csv
from pymongo import MongoClient

def extract_and_load(database_name):
    try:
        # Connexion à PostgreSQL
        pg_conn = psycopg2.connect(database=database_name, user="postgres", password="Gaoussou2002", host="localhost")
        pg_cursor = pg_conn.cursor()

        # Exécution de la requête pour obtenir les données en format JSON
        pg_cursor.execute("""
            SELECT json_agg(row_to_json(t))
            FROM (
                SELECT film_id, title, description, language_id, original_language_id,
                    (
                        SELECT json_agg(row_to_json(a))
                        FROM (
                            SELECT actor.actor_id, actor.first_name, actor.last_name
                            FROM actor
                            INNER JOIN film_actor ON actor.actor_id = film_actor.actor_id
                            WHERE film_actor.film_id = film.film_id
                        ) a
                    ) as actors
                FROM film
            ) t;
        """)
        rows = pg_cursor.fetchone()[0]  # Prendre le premier résultat qui devrait être une liste JSON

        # Vérifier que rows n'est pas None et insérer dans MongoDB
        if rows:
            collection.insert_many(rows)
        else:
            print(f"Aucune donnée à importer de {database_name}.")

    except Exception as e:
        print(f"Une erreur s'est produite avec la base de données {database_name}: {e}")
    finally:
        if pg_cursor:
            pg_cursor.close()
        if pg_conn:
            pg_conn.close()

def get_processed_databases(csv_file_path):
    try:
        with open(csv_file_path, mode='r', newline='') as file:
            reader = csv.reader(file)
            processed_databases = list(reader)[0]  # Assumer que le fichier CSV a une seule ligne avec les noms des BD
        return processed_databases
    except FileNotFoundError:
        return []  # Aucune base de données traitée si le fichier n'existe pas

def append_to_csv(csv_file_path, database_name):
    with open(csv_file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([database_name])

def get_all_pagila_databases(pg_conn):
    databases = []
    with pg_conn.cursor() as cur:
        cur.execute("SELECT datname FROM pg_database WHERE datname LIKE 'pagila%';")
        databases = [db[0] for db in cur.fetchall()]
    return databases

# Définition des chemins et des connexions
csv_file_path = 'C:/Users/gaous/Desktop/BUT 3/S5/SAE 5.02/Kamel/archive_pagila.csv'
client = MongoClient('localhost', 27017)
db = client['Pagila_db']
mongo_collection = db['Pagila_']
pg_conn = psycopg2.connect(database="postgres", user="postgres", password="Gaoussou2002", host="localhost")

# Obtenir les bases de données déjà traitées et toutes les bases Pagila
processed_databases = get_processed_databases(csv_file_path)
all_pagila_databases = get_all_pagila_databases(pg_conn)

# Filtrer les bases de données Pagila qui n'ont pas encore été traitées
unprocessed_databases = [db for db in all_pagila_databases if db not in processed_databases]

# Traitement des bases de données non traitées
for database_name in unprocessed_databases:
    extract_and_load(pg_conn, database_name, mongo_collection)
    append_to_csv(csv_file_path, database_name)

# Fermeture des connexions
pg_conn.close()
client.close()
print("Importation terminée pour toutes les nouvelles bases de données.")


# ... (Votre code précédent)

# Connexion à MongoDB
client = MongoClient('localhost', 27017)
db = client['Pagila_db']
collection = db['Pagila_']

# Affichage des 5 premiers documents de la collection films
for document in collection.find().limit(1):
    print(document)

# Fermeture de la connexion
client.close()


