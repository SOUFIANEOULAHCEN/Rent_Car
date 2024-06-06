from flask import Flask, request,session,render_template, redirect, url_for, flash
from datetime import datetime
from main import *
import sqlite3 as sql
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/img'
app.config['MAX_CONTENT_PATH'] = 10 * 1024 * 1024
app.secret_key = 'Soufiane' 

def get_db_connection():
    # Establish a connection to the database
    conn = sql.connect('Location.db')
    conn.row_factory = sql.Row
    return conn
# !-----------Index template principal ------------------
@app.route("/")
def index():
    # Establish a connection to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch available cars from the database
    # cursor.execute('SELECT id_voiture, marque, modele, path, categorie, prix FROM voiture')
    cursor.execute('SELECT * FROM voiture LIMIT 6')

    voitures = cursor.fetchall()

    # Close the connection
    conn.close()

    # Render the index.html template, passing the list of cars as context
    return render_template("index.html", voitures=voitures)


#!-----------------------Dahboard Admin------------------- -------------
@app.route('/Dashboard_Admin')
def Dashboard_Admin():
    connexion = sql.connect("Location.db")
    cursor = connexion.cursor()
    cursor.execute(''' SELECT count(*) FROM manager''')
    Number_Of_Managers = cursor.fetchone()
    cursor.execute(''' SELECT count(*) FROM  voiture''')
    NumberCars= cursor.fetchone()
    connexion.commit()
    connexion.close()
    admin = Administrateur("Oulahcen", "Soufiane", "soufiane@gmail.com", "motdepasse123")
    # Fetch the list of managers from the database
    idAdmin = Administrateur.get_idAdmin(admin)  # Get the admin ID
    managers = Administrateur.get_managers(idAdmin)  # Get the list of managers
    
    # Pass the list of managers to the template
    return render_template("Dashboard_Admin.html", managers=managers , Number_Of_Managers = Number_Of_Managers , NumberCars = NumberCars)

#!-------------------------Dashboard car for Admin----------------- -------------
@app.route('/Dashboard_Car')
def Dashboard_Car():
    connexion = sql.connect("Location.db")
    cursor = connexion.cursor()
    cursor.execute(''' SELECT * FROM voiture''')
    Cars = cursor.fetchall()
    cursor.execute(''' SELECT count(*) FROM  voiture''')
    NumberCars= cursor.fetchone()
    Available = '1'
    cursor.execute(''' SELECT count(*) FROM  voiture WHERE disponibilite = ?''',(Available,))
    NbrAvailable = cursor.fetchone()
    connexion.commit()
    connexion.close()
    return render_template('DashboardCar.html'  , Cars = Cars , NumberCars = NumberCars , NbrAvailable = NbrAvailable )
#!------------------------Add manager------------------ -------------
@app.route('/add_manager', methods=["POST"])
def add_manager():
    # Récupérer les données du formulaire
    nom = request.form["Lname"]
    prenom = request.form["Fname"]
    email = request.form["email"]
    motdepasse = request.form.get("motdepasse")  # Ajoutez un champ pour le mot de passe si nécessaire

    # Assurez-vous d'obtenir l'ID de l'administrateur associé
    admin = Administrateur("Oulahcen", "Soufiane", "soufiane@gmail.com", "motdepasse123")
    idAdmin = Administrateur.get_idAdmin(admin)
    
    # Ouvrir une connexion à la base de données
    connexion = sql.connect("Location.db")
    cursor = connexion.cursor()

    # Insérer le nouveau manager dans la base de données
    cursor.execute(
        '''INSERT INTO manager (nom, prenom, email, PSWD, id_admin) VALUES (?, ?, ?, ?, ?)''',
        (nom, prenom, email, motdepasse, idAdmin)
    )

    # Valider les modifications et fermer la connexion
    connexion.commit()
    connexion.close()

    # Rediriger vers le Dashboard Admin pour voir la liste mise à jour des managers
    return redirect(url_for('Dashboard_Admin'))


#!--------------------Edit Manager---------------------- -------------
@app.route('/edit_manager/<int:manager_id>', methods=["GET", "POST"])
def edit_manager(manager_id):
    # Vérifiez si la méthode de la requête est POST
    if request.method == "POST":
        # Récupérez les données du formulaire POST
        nom = request.form["Lname"]
        prenom = request.form["Fname"]
        email = request.form["email"]
        motdepasse = request.form["motdepasse"]

        # Mettez à jour les données du manager dans la base de données
        connexion = sql.connect("Location.db")
        cursor = connexion.cursor()
        cursor.execute(
            '''UPDATE manager SET nom = ?, prenom = ?, email = ?, PSWD = ? WHERE id_manager = ?''',
            (nom, prenom, email, motdepasse, manager_id)
        )
        connexion.commit()
        connexion.close()

        # Redirigez vers le Dashboard_Admin pour afficher la liste mise à jour des managers
        return redirect(url_for('Dashboard_Admin'))
    else:
        # Requête GET : affichez le formulaire prérempli avec les informations existantes du manager
        connexion = sql.connect("Location.db")
        cursor = connexion.cursor()
        cursor.execute('''SELECT nom, prenom, email, PSWD FROM manager WHERE id_manager = ?''', (manager_id,))
        manager = cursor.fetchone()
        connexion.close()

        # Vérifiez si le manager existe
        if not manager:
            return "Manager not found", 404
        
        # Affichez le formulaire de modification avec les données existantes
        return render_template('edit_manager.html', manager=manager, manager_id=manager_id)


#!------------------Delete manager------------------------ -------------
@app.route('/delete_manager/<int:manager_id>')
def delete_manager(manager_id):
    admin = Administrateur("Oulahcen", "Soufiane", "soufiane@gmail.com", "motdepasse123")
    idAdmin = Administrateur.get_idAdmin(admin)
    # result = admin.delete_manager(id)
    Administrateur.delete_manager(manager_id, idAdmin)

    return redirect(url_for('Dashboard_Admin'))


#!------------------------------------------ -------------
#!------------------------------------------ -------------
#!------------------------------------------ -------------
#!------------------------Dahboard for Manager------------------ -------------
@app.route('/Dashboard_Manager')
def Dashboard_Manager():
    # Ouvrir une connexion à la base de données
    connexion = sql.connect("Location.db")
    cursor = connexion.cursor()
    
    # Exécuter une requête pour obtenir toutes les voitures
    cursor.execute('''SELECT * FROM voiture''')
    
    # Obtenir toutes les voitures de la base de données
    voitures = cursor.fetchall()
    cursor.execute('''SELECT count(*) FROM voiture''')
    Nombre_voiture = cursor.fetchone()
    available = '1'
    cursor.execute('''SELECT count(*) FROM voiture WHERE disponibilite = ?''',(available,))
    Nombre_available = cursor.fetchone()

    
    # Fermer la connexion
    connexion.close()
    
    # Rendre le template avec les données des voitures
    return render_template('DashboardManager.html', voitures=voitures , Nombre_voiture=Nombre_voiture , Nombre_available = Nombre_available)



#!----------------------Add Car-------------------- -------------

@app.route('/add-car', methods=['POST'])
def add_car():
    # Récupération des données du formulaire
    marque = request.form['marque']
    modele = request.form['modele']
    immatriculation = request.form['immatriculation']
    categorie = request.form['categorie']
    prix = request.form['prix']
    disponibilite = request.form['disponibilite']
    photo = request.files.get('photo')

    # Répertoire où les photos sont stockées
    photo_dir = os.path.join('static', 'img')
    if not os.path.exists(photo_dir):
        os.makedirs(photo_dir)
    
    # Initialisation du chemin de la photo
    photo_path = 'img/default.jpg'
    
    # Téléchargement de la photo
    if photo and photo.filename:
        # Générer un chemin pour la photo
        file_path = os.path.join(photo_dir, photo.filename)
        
        # Sauvegarde de la photo dans le répertoire
        try:
            photo.save(file_path)
            
            # Conversion du chemin absolu en chemin relatif pour la base de données
            photo_path = os.path.relpath(file_path, 'static')
            
            # Normaliser le chemin de la photo pour éviter les barres obliques inversées
            photo_path = os.path.normpath(photo_path)
            photo_path = photo_path.replace('\\', '/')  # Remplacer les barres obliques inversées
            
        except Exception as e:
            print(f"Erreur lors du téléchargement de la photo: {e}")
    
    # Connexion à la base de données
    conn = None
    try:
        conn = sql.connect("Location.db")
        cursor = conn.cursor()
        
        # Insertion des données dans la table `voiture`
        cursor.execute("""
            INSERT INTO voiture (marque, modele, immatriculation, categorie, prix, disponibilite, path)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (marque, modele, immatriculation, categorie, prix, disponibilite, photo_path))
        
        # Enregistrer les modifications
        conn.commit()
        
    except Exception as e:
        print(f"Erreur lors de l'insertion dans la base de données: {e}")
    
    finally:
        # Fermeture de la connexion à la base de données
        if conn:
            conn.close()
    
    # Redirection vers le tableau de bord du gestionnaire
    return redirect(url_for('Dashboard_Manager'))


#!------------------------------------------ -------------
#!------------------------------------------ -------------

#!------------------------Edit Car------------------ -------------
@app.route('/edit-car-form/<int:car_id>', methods=['GET', 'POST'])
def edit_car_form(car_id):
    conn = sql.connect("Location.db")
    cursor = conn.cursor()
    
    # Si la méthode de requête est POST, traiter les données du formulaire
    if request.method == 'POST':
        marque = request.form['marque']
        modele = request.form['modele']
        immatriculation = request.form['immatriculation']
        categorie = request.form['categorie']
        prix = request.form['prix']
        disponibilite = request.form['disponibilite']
        
        # Si une nouvelle photo est soumise, enregistrez-la et mettez à jour le chemin
        photo = request.files.get('photo')
        if photo and photo.filename:
            # Générer un chemin pour la photo
            photo_path = os.path.join(app.config['UPLOAD_FOLDER'], photo.filename)
            
            # Enregistrer la photo dans le dossier spécifié
            photo.save(photo_path)
            
            # Convertir le chemin absolu en chemin relatif
            photo_path = os.path.relpath(photo_path, 'static')
        
        else:
            # Si aucune nouvelle photo n'est soumise, utilisez l'ancien chemin
            photo_path = request.form['current_photo']
        
        # Assurez-vous de remplacer les barres obliques inversées par des barres obliques normales
        photo_path = photo_path.replace('\\', '/')

        # Mettre à jour les détails de la voiture dans la base de données
        cursor.execute("""
            UPDATE voiture
            SET marque = ?, modele = ?, immatriculation = ?, categorie = ?, prix = ?, disponibilite = ?, path = ?
            WHERE id_voiture = ?
        """, (marque, modele, immatriculation, categorie, prix, disponibilite, photo_path, car_id))
        
        conn.commit()
        conn.close()

        # Rediriger vers le tableau de bord
        return redirect(url_for('Dashboard_Manager'))
    
    # Si la méthode de requête est GET, afficher le formulaire de modification de voiture
    cursor.execute("SELECT * FROM voiture WHERE id_voiture = ?", (car_id,))
    voiture = cursor.fetchone()
    conn.close()

    if voiture:
        return render_template('edit_car_form.html', voiture=voiture)
    else:
        return "Voiture non trouvée", 404

#!------------------------Delete Car------------------ -------------
@app.route('/delete-car/<int:car_id>', methods=['POST'])
def delete_car(car_id):
    conn = sql.connect("Location.db")
    cursor = conn.cursor()

    # Supprimer la voiture de la base de données
    cursor.execute("DELETE FROM voiture WHERE id_voiture = ?", (car_id,))
    
    conn.commit()
    conn.close()

    # Rediriger vers le tableau des voitures
    return redirect(url_for('Dashboard_Manager'))
#!------------------------------------------ -------------
#!------------------------------------------ -------------


# !====================fix here ???!!!! 
#!----------------------Resrvations-------------------- -------------

@app.route('/reserve', methods=['GET', 'POST'])
def reserve():
    if request.method == 'POST':
        # Get form data
        nom = request.form['nom'].strip()
        prenom = request.form['prenom'].strip()
        email = request.form['email'].strip()
        telephone = request.form['telephone'].strip()
        voiture_id = request.form['voiture_id']
        date_debut = request.form['date_debut'].strip()
        date_fin = request.form['date_fin'].strip()

        # # Validate the form data
        # if not all([nom, prenom, email, telephone, voiture_id, date_debut, date_fin]):
        #     flash('Tous les champs sont obligatoires.', 'error')
        #     return redirect(url_for('reserve'))
        # Convert date_debut and date_fin to datetime objects for easier comparison
        date_debut = datetime.strptime(date_debut, '%Y-%m-%d')
        date_fin = datetime.strptime(date_fin, '%Y-%m-%d')

        # Check date validity
        if date_debut >= date_fin:
            flash('La date de début doit être avant la date de fin.', 'error')
            return redirect(url_for('reserve'))

        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Add client to the database and get client ID
        cursor.execute('INSERT INTO client (nom, prenom, email, telephone) VALUES (?, ?, ?, ?)', (nom, prenom, email, telephone))
        conn.commit()

        # Get the last inserted client ID
        client_id = cursor.lastrowid

        # Add reservation to the database using the client ID and voiture ID
        # cursor.execute('''
        #     INSERT INTO reservations (nom, prenom, email, telephone , id_client, voiture_id, date_debut, date_fin)
        #     VALUES (?, ?, ?, ?, ? ,? ,? ,?)
        # ''', (nom, prenom, email, telephone, client_id, voiture_id, date_debut, date_fin))
        cursor.execute('''
    INSERT INTO reservations (nom, prenom, email, telephone , id_client, voiture_id, date_debut, date_fin)
    VALUES (?, ?, ?, ?, ? ,? ,? ,?)
''', (nom, prenom, email, telephone, client_id, voiture_id, date_debut, date_fin))
        conn.commit()

        # Close the connection
        conn.close()
        return redirect(url_for('index'))

    # For GET requests, render the form template
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch available cars from the database
    cursor.execute('SELECT id_voiture, marque, modele FROM voiture')
    voitures = cursor.fetchall()

    conn.close()

    return render_template('reservation_form.html', voitures=voitures)
  

#!----------------------- Dashboard reservation ------------------- -------------
@app.route("/dashboard/reservations")
def reservations_dashboard():
    # Establish a connection to the database
    # conn = get_db_connection()
    conn = sql.connect("Location.db")
    cursor = conn.cursor()

    # Fetch all reservations from the database
    # This query joins the reservations table with voiture and client tables
    # Modify the column names according to your table structure
    cursor.execute(''' 
                   SELECT * FROM reservations
                   ''')
    # cursor.execute("""
    #     SELECT
    #         r.id AS reservation_id,
    #         c.nom AS client_nom,
    #         c.prenom AS client_prenom,
    #         c.email AS client_email,
    #         c.telephone AS client_telephone,
    #         v.marque AS voiture_marque,
    #         v.modele AS voiture_modele,
    #         r.date_debut,
    #         r.date_fin
    #     FROM
    #         reservations AS r
    #     JOIN
    #         client AS c ON r.id_client = c.id_client
    #     JOIN
    #         voiture AS v ON r.voiture_id = v.id_voiture
    # """)

    # Fetch all rows from the query
    reservations = cursor.fetchall()

    # Close the database connection
    conn.close()

    # Render the dashboard_reservations.html template, passing the reservations list as context
    return render_template("dashboard_reservations.html", reservations=reservations)



#!------------------------reservation actions------------------ -------------
@app.route("/reservations/<int:reservation_id>/accept", methods=["POST"])
def accept_reservation(reservation_id):
    # Establish a connection to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Accept the reservation by updating its status
    # Update the reservation status as needed (you may want to add a 'status' column to the 'reservations' table)
    cursor.execute('UPDATE reservations SET status = "accepted" WHERE id = ?', (reservation_id,))
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    # Return a successful response
    return "", 200

@app.route("/reservations/<int:reservation_id>/refuse", methods=["POST"])
def refuse_reservation(reservation_id):
    # Establish a connection to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Refuse the reservation by updating its status
    # Update the reservation status as needed (you may want to add a 'status' column to the 'reservations' table)
    cursor.execute('UPDATE reservations SET status = "refused" WHERE id = ?', (reservation_id,))
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    # Return a successful response
    return "", 200

#!------------------------------------------ -------------
#!------------------------------------------ -------------
#!------------------------------------------ -------------
#!------------------------------------------ -------------
#!------------------------------------------ -------------
#!------------------------Login ------------------ -------------


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Connexion à la base de données
        connexion = sql.connect("Location.db")
        cursor = connexion.cursor()
        
        # Vérification des informations d'identification dans la table 'administrateur'
        cursor.execute('''SELECT * FROM administrateur WHERE email = ? AND PSWD = ?''', (username, password))
        admin = cursor.fetchone()
        
        # Si l'utilisateur est un administrateur
        if admin:
            session['username'] = username  # Stocker le nom d'utilisateur dans la session
            return redirect(url_for('Dashboard_Admin'))  # Rediriger vers le tableau de bord de l'administrateur
        
        # Vérification si l'utilisateur est un gestionnaire
        cursor.execute('''SELECT * FROM manager WHERE email = ? AND PSWD = ?''', (username, password))
        manager = cursor.fetchone()
        
        # Si l'utilisateur est un gestionnaire
        if manager:
            session['username'] = username  # Stocker le nom d'utilisateur dans la session
            return redirect(url_for('Dashboard_Manager'))  # Rediriger vers le tableau de bord du gestionnaire
        
        # Si les informations d'identification sont incorrectes, afficher un message d'erreur
        error = 'Invalid username or password'
        return render_template('login.html', error=error)
    else:
        # Afficher le formulaire de connexion si la méthode est GET
        return render_template('login.html')
#!------------------------------------------ -------------

if __name__ == "__main__":
    app.run(debug=True)