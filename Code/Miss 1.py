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

