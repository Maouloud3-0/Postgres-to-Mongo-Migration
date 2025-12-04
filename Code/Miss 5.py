# =============================================================================
# #  Mission 5
# =============================================================================
# =============================================================================

import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import customtkinter as ctk
from pymongo import MongoClient
import json

def add_actor():
    full_name = simpledialog.askstring("Acteur", "Entrez le nom complet de l'acteur (Prénom Nom):")
    if full_name:
        actors_listbox.insert(tk.END, full_name)

def edit_selected_actor():
    try:
        selected_index = actors_listbox.curselection()[0]
        selected_actor = actors_listbox.get(selected_index)
        new_name = simpledialog.askstring("Modifier l'acteur", "Modifier le nom de l'acteur:", initialvalue=selected_actor)
        if new_name:
            actors_listbox.delete(selected_index)
            actors_listbox.insert(selected_index, new_name)
    except IndexError:
        messagebox.showwarning("Attention", "Veuillez sélectionner un acteur à modifier.")

def delete_selected_actor():
    try:
        selected_index = actors_listbox.curselection()[0]
        actors_listbox.delete(selected_index)
    except IndexError:
        messagebox.showwarning("Attention", "Veuillez sélectionner un acteur à supprimer.")

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

def save_data_to_json(film_data, filepath="film_data.json"):
    try:
        with open(filepath, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []

    data.append(film_data)

    with open(filepath, 'w') as file:
        json.dump(data, file, indent=4)

def insert_data():
    actors = [{'first_name': actor.split(' ')[0], 'last_name': ' '.join(actor.split(' ')[1:])} for actor in actors_listbox.get(0, tk.END)]
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
        mongo_db.Pagila_.insert_one(film_data)
        messagebox.showinfo("Success", "Film data inserted successfully.")
        save_data_to_json(film_data)
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


# Configuration de l'interface utilisateur
root = ctk.CTk()
root.title("Saisie des données film")
root.minsize(600, 500)  # Définit une taille minimale pour la fenêtre

# Configurez la grille principale de la fenêtre
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)

# Cadre pour les informations sur le film
info_frame = ctk.CTkFrame(root)
info_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=10)
info_frame.grid_columnconfigure(1, weight=1)

# Définition des étiquettes et des champs de saisie pour les informations du film
film_id_label = ctk.CTkLabel(info_frame, text="Film ID")
film_id_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)
film_id_entry = ctk.CTkEntry(info_frame, width=200)
film_id_entry.grid(row=0, column=1, sticky="ew", padx=10, pady=10)

title_label = ctk.CTkLabel(info_frame, text="Titre")
title_label.grid(row=1, column=0, sticky="w", padx=10, pady=10)
title_entry = ctk.CTkEntry(info_frame, width=200)
title_entry.grid(row=1, column=1, sticky="ew", padx=10, pady=10)

description_label = ctk.CTkLabel(info_frame, text="Description")
description_label.grid(row=2, column=0, sticky="w", padx=10, pady=10)
description_entry = ctk.CTkEntry(info_frame, width=200)
description_entry.grid(row=2, column=1, sticky="ew", padx=10, pady=10)

language_id_label = ctk.CTkLabel(info_frame, text="Language ID")
language_id_label.grid(row=3, column=0, sticky="w", padx=10, pady=10)
language_id_entry = ctk.CTkEntry(info_frame, width=200)
language_id_entry.grid(row=3, column=1, sticky="ew", padx=10, pady=10)

original_language_id_label = ctk.CTkLabel(info_frame, text="Original Language ID")
original_language_id_label.grid(row=4, column=0, sticky="w", padx=10, pady=10)
original_language_id_entry = ctk.CTkEntry(info_frame, width=200)
original_language_id_entry.grid(row=4, column=1, sticky="ew", padx=10, pady=10)

# Cadre pour les acteurs
actors_frame = ctk.CTkFrame(root)
actors_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
actors_frame.grid_columnconfigure(0, weight=1)

actors_label = ctk.CTkLabel(actors_frame, text="Acteurs")
actors_label.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

actors_list_frame = ctk.CTkFrame(actors_frame)
actors_list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

actors_listbox = tk.Listbox(actors_list_frame, height=4)
actors_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(actors_list_frame, orient="vertical")
scrollbar.config(command=actors_listbox.yview)
scrollbar.pack(side="right", fill="y")

actors_listbox.config(yscrollcommand=scrollbar.set)

# Cadre pour les boutons
button_frame = ctk.CTkFrame(root)
button_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)

add_actor_button = ctk.CTkButton(button_frame, text='Ajouter Acteur', command=add_actor)
add_actor_button.pack(side=tk.LEFT, padx=10, pady=10)

edit_actor_button = ctk.CTkButton(button_frame, text='Modifier Acteur', command=edit_selected_actor)
edit_actor_button.pack(side=tk.LEFT, padx=10, pady=10)

delete_actor_button = ctk.CTkButton(button_frame, text='Supprimer Acteur', command=delete_selected_actor)
delete_actor_button.pack(side=tk.LEFT, padx=10, pady=10)

insert_button = ctk.CTkButton(button_frame, text='Insérer', command=insert_data)
insert_button.pack(side=tk.LEFT, padx=10, pady=10)

import_json_button = ctk.CTkButton(button_frame, text='Importer JSON', command=load_json)
import_json_button.pack(side=tk.LEFT, padx=10, pady=10)

root.mainloop()




#  !pyinstaller --onefile --windowed --name "Interface_minssion" "C:\Users\gaous\Desktop\BUT 3\S5\SAE 5.02\Kamel\Miss 5.py"