import sqlite3 as sql
import os


database_file = "Location.db"
connexion = sql.connect(database_file)
cursor = connexion.cursor()

# cursor.execute("""CREATE TABLE administrateur (
#                 id_admin INTEGER PRIMARY KEY AUTOINCREMENT,
#                 nom TEXT NOT NULL,
#                 prenom TEXT NOT NULL,
#                 email TEXT NOT NULL,
#                 PSWD TEXT NOT NULL )""")## created

# cursor.execute("""CREATE TABLE manager (
#                 id_manager INTEGER PRIMARY KEY AUTOINCREMENT,
#                 nom TEXT NOT NULL,
#                 prenom TEXT NOT NULL,
#                 email TEXT NOT NULL,
#                 PSWD TEXT NOT NULL,
#                 id_admin INTEGER,
#                 FOREIGN KEY (id_admin) REFERENCES administrateur(id_admin))""") ##craeted

# cursor.execute("""CREATE TABLE client (
#                 id_client INTEGER PRIMARY KEY AUTOINCREMENT,
#                 nom TEXT NOT NULL,
#                 prenom TEXT NOT NULL,
#                 email TEXT NOT NULL,
#                 telephone TEXT NOT NULL)""")##created
 
# cursor.execute(
#     """CREATE TABLE voiture (
#                 id_voiture INTEGER PRIMARY KEY AUTOINCREMENT,
#                 marque TEXT NOT NULL,
#                 modele TEXT NOT NULL,
#                 immatriculation TEXT NOT NULL,
#                 categorie TEXT NOT NULL,
#                 prix TEXT NOT NULL,
#                 disponibilite TEXT NOT NULL,
#                 path TEXT NOT NULL,
#                 id_manager INTEGER,
#                 id_client INTEGER,
#                 FOREIGN KEY (id_manager) REFERENCES manager(id_manager),
#                 FOREIGN KEY (id_client) REFERENCES client(id_client)
#     )"""
# )

# # Créer la table `reservations` avec la structure correcte
# cursor.execute("""
#     CREATE TABLE IF NOT EXISTS reservations (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         nom TEXT NOT NULL,
#         prenom TEXT NOT NULL,
#         email TEXT NOT NULL,
#         telephone TEXT NOT NULL,
#         voiture_id INTEGER NOT NULL,
#         date_debut DATE NOT NULL,
#         date_fin DATE NOT NULL,
#         id_client INTEGER NOT NULL,
#         FOREIGN KEY (voiture_id) REFERENCES voiture(id_voiture),
#         FOREIGN KEY (id_client) REFERENCES client(id_client)
#     )
# """)

# cursor.execute("DROP TABLE IF EXISTS administrateur")

# conn = sql.connect("Location.db")
# cursor = conn.cursor()

# Supprimer la table si elle existe
# cursor.execute("DROP TABLE IF EXISTS reservations")



connexion.commit()
connexion.close()


# cursor.execute('''  ''')



# query = """
# DROP FROM administrateur WHERE id_admin=2

# """

# # Valeurs à insérer
# nom = "Oulahcen"
# prenom = "Soufiane"
# email = "soufiane@gmail.com"
# pswd = "motdepasse123"  # Remplacez par le mot de passe souhaité

# # Exécutez la requête d'insertion
# # cursor.execute(insertion_query, (nom, prenom, email, pswd))
# query ='''DELETE FROM manager'''
# cursor.execute(query)

# connexion.commit()
# connexion.close()








# # Specify the path to the database file
# database_file = "Location.db"
# connexion = sql.connect(database_file)
# cursor = connexion.cursor()

# # Close the SQLite connection if it's open
# try:
#     connexion.close()
# except NameError:
#     pass  # Ignore if connexion is not defined

# # Check if the database file exists
# if os.path.exists(database_file):
#     # Delete the database file
#     os.remove(database_file)
#     print(f"The database file '{database_file}' has been deleted.")
# else:
#     print(f"The database file '{database_file}' does not exist.")