import psycopg2
import os
import glob

# =============================================================================
# # Les informations de connexion à la base de données PostgreSQL locale
# =============================================================================
db_params = {
    'database': 'postgres',
    'user': 'postgres',
    'password': 'Gaoussou2002',
    'host': 'localhost'
}

# =============================================================================
# # Le script SQL pour créer les tables
# =============================================================================
sql_commands = """
    CREATE TABLE public.film (
        film_id integer NOT NULL,
        title text NOT NULL,
        description text,
        language_id integer NOT NULL,
        original_language_id text NULL
    );

    ALTER TABLE public.film OWNER TO postgres;

    CREATE TABLE public.actor (
        actor_id integer NOT NULL,
        first_name text NOT NULL,
        last_name text NOT NULL
    );

    ALTER TABLE public.actor OWNER TO postgres;

    CREATE TABLE public.film_actor (
        actor_id integer NOT NULL,
        film_id integer NOT NULL
    );

    ALTER TABLE public.film_actor OWNER TO postgres;
"""

# =============================================================================
# # Les noms des bases de données à créer
# =============================================================================
db_names = ['pagila1', 'pagila2', 'pagila3', 'pagila4', 'pagila5']

def create_db(db_name):
    params = db_params.copy()
    params['database'] = 'postgres'
    
    # Créer une nouvelle connexion sans utiliser le gestionnaire de contexte 'with'
    conn = psycopg2.connect(**params)
    conn.autocommit = True
    
    with conn.cursor() as cur:
        cur.execute(f"DROP DATABASE IF EXISTS {db_name};")
        cur.execute(f"CREATE DATABASE {db_name};")
    
    # Fermer la connexion
    conn.close()




# =============================================================================
# # Fonction pour exécuter le script SQL dans une base de données spécifique
# =============================================================================
def create_tables(db_name):
    db_params['database'] = db_name
    with psycopg2.connect(**db_params) as conn:
        with conn.cursor() as cur:
            cur.execute(sql_commands)



# =============================================================================
# # Création des bases de données et des tables
# =============================================================================
for db_name in db_names:
    create_db(db_name)
    create_tables(db_name)



# =============================================================================
#  Importation des données sur dans pagilas 1
# =============================================================================
import psycopg2
import os

# Les informations de connexion à la base de données PostgreSQL locale pour pagila1
db_params = {
    'database': 'pagila1',
    'user': 'postgres',
    'password': 'Gaoussou2002',  # Changez ceci pour votre mot de passe réel
    'host': 'localhost'
}

# =============================================================================
# # Chemin d'accès où se trouvent vos fichiers CSV pour pagila1
# =============================================================================
csv_folder_path = 'C:/Users/gaous/Desktop/BUT 3/S5/SAE 5.02/Kamel/Données-20231129/Fichiers csv'

def populate_db(table_name, csv_file):
    with psycopg2.connect(**db_params) as conn:
        with conn.cursor() as cur:
            with open(csv_file, 'r') as f:
                next(f)  # Skip the header line
                cur.copy_from(f, table_name, sep=',', null='\\N')  # Ajout de la gestion des NULL


# =============================================================================
# # Noms des fichiers CSV spécifiques pour pagila1
# =============================================================================
csv_files = {
    'actor': os.path.join(csv_folder_path, 'actor1.csv'),
    'film_actor': os.path.join(csv_folder_path, 'film_actor1.csv'),
    'film': os.path.join(csv_folder_path, 'film1.csv')
}

# =============================================================================
# # Insertion des données des fichiers CSV dans la base de données pagila1
# =============================================================================
for table_name, csv_file in csv_files.items():
    populate_db(table_name, csv_file)

print("Les données ont été insérées avec succès dans la base de données pagila1.")


# =============================================================================
# =============================================================================
# =============================================================================
# # #       Importer les données automatiquement sur postegres 
# =============================================================================
# =============================================================================
# =============================================================================


import psycopg2
import os

# =============================================================================
# # Chemin d'accès où se trouvent vos fichiers CSV
# =============================================================================
csv_folder_path = 'C:/Users/gaous/Desktop/BUT 3/S5/SAE 5.02/Kamel/Données-20231129/Fichiers csv'

# =============================================================================
# # Paramètres de connexion communs à toutes les bases de données
# =============================================================================
common_db_params = {
    'user': 'postgres',
    'password': 'Gaoussou2002',  # Remplacez par votre mot de passe réel
    'host': 'localhost'
}

def populate_db(db_name, table_name, csv_file):
    db_params = common_db_params.copy()
    db_params['database'] = db_name
    with psycopg2.connect(**db_params) as conn:
        with conn.cursor() as cur:
            with open(csv_file, 'r') as f:
                next(f)  # Skip the header line
                cur.copy_from(f, table_name, sep=',', null='\\N')  # Ajout de la gestion des NULL

# =============================================================================
# # Liste des noms de bases de données
# =============================================================================
db_names = ['pagila1', 'pagila2', 'pagila3', 'pagila4', 'pagila5']

# =============================================================================
# # Boucle sur chaque base de données pour insérer les données
# =============================================================================
for i, db_name in enumerate(db_names, start=1):
    print(f"Insertion des données dans la base de données {db_name}...")
    
# =============================================================================
#     # Noms des fichiers CSV spécifiques pour chaque base de données
# =============================================================================
    csv_files = {
        'actor': os.path.join(csv_folder_path, f'actor{i}.csv'),
        'film_actor': os.path.join(csv_folder_path, f'film_actor{i}.csv'),
        'film': os.path.join(csv_folder_path, f'film{i}.csv')
    }
    
# =============================================================================
#     # Insertion des données des fichiers CSV dans la base de données courante
# =============================================================================
    for table_name, csv_file in csv_files.items():
        populate_db(db_name, table_name, csv_file)

    print(f"Les données ont été insérées avec succès dans la base de données {db_name}.")


# =============================================================================
# =============================================================================
# =============================================================================
# # #  Mission trois 
# =============================================================================
# =============================================================================
# =============================================================================

from pymongo import MongoClient
import psycopg2
import json

try:
    # Connexion à PostgreSQL
    pg_conn = psycopg2.connect(database="pagila1", user="postgres", password="Gaoussou2002", host="localhost")
    pg_cursor = pg_conn.cursor()

    # Exécution de la requête pour obtenir les données en format JSON
    pg_cursor.execute(""" SELECT json_agg(row_to_json(t))
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
) t; """)
    rows = pg_cursor.fetchall()

    # Connexion à MongoDB
    client = MongoClient('localhost', 27017)
    db = client['Pagila_db']
    collection = db['Pagila_']

    # Insertion des données dans MongoDB
    for row in rows:
        json_str = row[0]  # row[0] doit être une chaîne JSON
        if isinstance(json_str, str):
            film_data = json.loads(json_str)
            if isinstance(film_data, list):
                collection.insert_many()
            else:
                collection.insert_one(film_data)
        else:
            print("La donnée n'est pas une chaîne JSON valide.")

    print("Importation terminée.")
    
except Exception as e:
    print(f"Une erreur s'est produite: {e}")
finally:
    pg_cursor.close()
    pg_conn.close()
    client.close()

# =============================================================================
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
# =============================================================================
# #  Mission 5
# =============================================================================
# =============================================================================
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, Listbox, Button, Label, Entry, Frame
from pymongo import MongoClient
import json

def add_actor():
    actor_first_name = simpledialog.askstring("Acteur", "Prénom de l'acteur:")
    actor_last_name = simpledialog.askstring("Acteur", "Nom de l'acteur:")
    if actor_first_name and actor_last_name:
        actors_listbox.insert(tk.END, f"{actor_first_name} {actor_last_name}")

def insert_data_from_json(filepath):
    with open(filepath, 'r') as file:
        film_data = json.load(file)
    try:
        mongo_client = MongoClient("mongodb://localhost:27017/")
        mongo_db = mongo_client["pagila"]
        mongo_db.Pagila_.insert_one(film_data)
        messagebox.showinfo("Success", "Film data inserted from JSON successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while inserting JSON data: {e}")
    finally:
        mongo_client.close()

def insert_data():
    actors = [{'first_name': actor.split(' ')[0], 'last_name': actor.split(' ')[1]} for actor in actors_listbox.get(0, tk.END)]
    film_data = {
        "film_id": film_id_entry.get(),
        "title": title_entry.get(),
        "description": description_entry.get(),
        "language_id": language_id_entry.get(),
        "original_language_id": original_language_id_entry.get() or None,
        "actors": actors
    }

    if not (film_data["film_id"] and film_data["title"]):
        messagebox.showwarning("Warning", "Film ID and Title are required.")
        return

    try:
        mongo_client = MongoClient("mongodb://localhost:27017/")
        mongo_db = mongo_client["pagila"]
        result = mongo_db.Pagila_.insert_one(film_data)
        inserted_data = mongo_db.Pagila_.find_one({'_id': result.inserted_id})
        messagebox.showinfo("Success", f"Film data inserted successfully: {inserted_data}")
        clear_entries()
        actors_listbox.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
    finally:
        mongo_client.close()

def clear_entries():
    film_id_entry.delete(0, tk.END)
    title_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)
    language_id_entry.delete(0, tk.END)
    original_language_id_entry.delete(0, tk.END)

def load_json():
    filepath = filedialog.askopenfilename(
        title="Open JSON File",
        filetypes=[("JSON files", "*.json")]
    )
    if filepath:
        insert_data_from_json(filepath)

root = tk.Tk()
root.title("Saisie des données film")

Label(root, text="Film ID").grid(row=0)
Label(root, text="Titre").grid(row=1)
Label(root, text="Description").grid(row=2)
Label(root, text="Language ID").grid(row=3)
Label(root, text="Original Language ID").grid(row=4)
Label(root, text="Acteurs").grid(row=5)

film_id_entry = Entry(root)
title_entry = Entry(root)
description_entry = Entry(root)
language_id_entry = Entry(root)
original_language_id_entry = Entry(root)

film_id_entry.grid(row=0, column=1)
title_entry.grid(row=1, column=1)
description_entry.grid(row=2, column=1)
language_id_entry.grid(row=3, column=1)
original_language_id_entry.grid(row=4, column=1)

actors_frame = Frame(root)
actors_frame.grid(row=5, column=1, sticky='ew')
actors_listbox = Listbox(actors_frame)
actors_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
Button(actors_frame, text='Ajouter Acteur', command=add_actor).pack(side=tk.RIGHT)

Button(root, text='Insérer', command=insert_data).grid(row=6, column=0, sticky=tk.W, pady=4)
Button(root, text='Importer JSON', command=load_json).grid(row=6, column=1, sticky=tk.W, pady=4)

root.mainloop()


