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
