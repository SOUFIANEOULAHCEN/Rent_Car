from flask import Flask, request, session, render_template, redirect, url_for, flash
from datetime import datetime
from main import *
import sqlite3 as sql
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/img'
app.config['MAX_CONTENT_PATH'] = 10 * 1024 * 1024
app.secret_key = 'Soufiane' 

def get_db_connection():
    conn = sql.connect('Location.db')
    conn.row_factory = sql.Row
    return conn

@app.route("/")
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM voiture LIMIT 6')
    voitures = cursor.fetchall()
    conn.close()
    return render_template("index.html", voitures=voitures)

@app.route('/Dashboard_Admin')
def Dashboard_Admin():
    conn = sql.connect("Location.db")
    cursor = conn.cursor()
    cursor.execute('SELECT count(*) FROM manager')
    Number_Of_Managers = cursor.fetchone()
    cursor.execute('SELECT count(*) FROM voiture')
    NumberCars = cursor.fetchone()
    conn.commit()
    conn.close()
    admin = Administrateur("Oulahcen", "Soufiane", "soufiane@gmail.com", "motdepasse123")
    idAdmin = Administrateur.get_idAdmin(admin)
    managers = Administrateur.get_managers(idAdmin)
    return render_template("Dashboard_Admin.html", managers=managers, Number_Of_Managers=Number_Of_Managers, NumberCars=NumberCars)

@app.route('/Dashboard_Car')
def Dashboard_Car():
    conn = sql.connect("Location.db")
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM voiture')
    Cars = cursor.fetchall()
    cursor.execute('SELECT count(*) FROM voiture')
    NumberCars = cursor.fetchone()
    Available = '1'
    cursor.execute('SELECT count(*) FROM voiture WHERE disponibilite = ?', (Available,))
    NbrAvailable = cursor.fetchone()
    conn.commit()
    conn.close()
    return render_template('DashboardCar.html', Cars=Cars, NumberCars=NumberCars, NbrAvailable=NbrAvailable)

@app.route('/add_manager', methods=["POST"])
def add_manager():
    nom = request.form["Lname"]
    prenom = request.form["Fname"]
    email = request.form["email"]
    motdepasse = request.form.get("motdepasse")
    admin = Administrateur("Oulahcen", "Soufiane", "soufiane@gmail.com", "motdepasse123")
    idAdmin = Administrateur.get_idAdmin(admin)
    conn = sql.connect("Location.db")
    cursor = conn.cursor()
    cursor.execute('INSERT INTO manager (nom, prenom, email, PSWD, id_admin) VALUES (?, ?, ?, ?, ?)', (nom, prenom, email, motdepasse, idAdmin))
    conn.commit()
    conn.close()
    return redirect(url_for('Dashboard_Admin'))

@app.route('/edit_manager/<int:manager_id>', methods=["GET", "POST"])
def edit_manager(manager_id):
    if request.method == "POST":
        nom = request.form["Lname"]
        prenom = request.form["Fname"]
        email = request.form["email"]
        motdepasse = request.form["motdepasse"]
        conn = sql.connect("Location.db")
        cursor = conn.cursor()
        cursor.execute('UPDATE manager SET nom = ?, prenom = ?, email = ?, PSWD = ? WHERE id_manager = ?', (nom, prenom, email, motdepasse, manager_id))
        conn.commit()
        conn.close()
        return redirect(url_for('Dashboard_Admin'))
    else:
        conn = sql.connect("Location.db")
        cursor = conn.cursor()
        cursor.execute('SELECT nom, prenom, email, PSWD FROM manager WHERE id_manager = ?', (manager_id,))
        manager = cursor.fetchone()
        conn.close()
        if not manager:
            return "Manager not found", 404
        return render_template('edit_manager.html', manager=manager, manager_id=manager_id)

@app.route('/delete_manager/<int:manager_id>')
def delete_manager(manager_id):
    admin = Administrateur("Oulahcen", "Soufiane", "soufiane@gmail.com", "motdepasse123")
    idAdmin = Administrateur.get_idAdmin(admin)
    Administrateur.delete_manager(manager_id, idAdmin)
    return redirect(url_for('Dashboard_Admin'))

@app.route('/Dashboard_Manager')
def Dashboard_Manager():
    conn = sql.connect("Location.db")
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM voiture')
    voitures = cursor.fetchall()
    cursor.execute('SELECT count(*) FROM voiture')
    Nombre_voiture = cursor.fetchone()
    available = '1'
    cursor.execute('SELECT count(*) FROM voiture WHERE disponibilite = ?', (available,))
    Nombre_available = cursor.fetchone()
    conn.close()
    return render_template('DashboardManager.html', voitures=voitures, Nombre_voiture=Nombre_voiture, Nombre_available=Nombre_available)

@app.route('/add-car', methods=['POST'])
def add_car():
    marque = request.form['marque']
    modele = request.form['modele']
    immatriculation = request.form['immatriculation']
    categorie = request.form['categorie']
    prix = request.form['prix']
    disponibilite = request.form['disponibilite']
    photo = request.files.get('photo')
    photo_dir = os.path.join('static', 'img')
    if not os.path.exists(photo_dir):
        os.makedirs(photo_dir)
    photo_path = 'img/default.jpg'
    if photo and photo.filename:
        file_path = os.path.join(photo_dir, photo.filename)
        try:
            photo.save(file_path)
            photo_path = os.path.relpath(file_path, 'static')
            photo_path = os.path.normpath(photo_path)
            photo_path = photo_path.replace('\\', '/')
        except Exception as e:
            print(f"Erreur lors du téléchargement de la photo: {e}")
    conn = sql.connect("Location.db")
    cursor = conn.cursor()
    cursor.execute('INSERT INTO voiture (marque, modele, immatriculation, categorie, prix, disponibilite, path) VALUES (?, ?, ?, ?, ?, ?, ?)', (marque, modele, immatriculation, categorie, prix, disponibilite, photo_path))
    conn.commit()
    conn.close()
    return redirect(url_for('Dashboard_Manager'))

@app.route('/edit-car-form/<int:car_id>', methods=['GET', 'POST'])
def edit_car_form(car_id):
    conn = sql.connect("Location.db")
    cursor = conn.cursor()
    if request.method == 'POST':
        marque = request.form['marque']
        modele = request.form['modele']
        immatriculation = request.form['immatriculation']
        categorie = request.form['categorie']
        prix = request.form['prix']
        disponibilite = request.form['disponibilite']
        photo = request.files.get('photo')
        if photo and photo.filename:
            photo_dir = os.path.join('static', 'img')
            if not os.path.exists(photo_dir):
                os.makedirs(photo_dir)
            file_path = os.path.join(photo_dir, photo.filename)
            try:
                photo.save(file_path)
                photo_path = os.path.relpath(file_path, 'static')
                photo_path = os.path.normpath(photo_path)
                photo_path = photo_path.replace('\\', '/')
            except Exception as e:
                print(f"Erreur lors du téléchargement de la photo: {e}")
        else:
            photo_path = None
        if photo_path:
            cursor.execute('UPDATE voiture SET marque = ?, modele = ?, immatriculation = ?, categorie = ?, prix = ?, disponibilite = ?, path = ? WHERE id_voiture = ?', (marque, modele, immatriculation, categorie, prix, disponibilite, photo_path, car_id))
        else:
            cursor.execute('UPDATE voiture SET marque = ?, modele = ?, immatriculation = ?, categorie = ?, prix = ?, disponibilite = ? WHERE id_voiture = ?', (marque, modele, immatriculation, categorie, prix, disponibilite, car_id))
        conn.commit()
        conn.close()
        return redirect(url_for('Dashboard_Manager'))
    else:
        cursor.execute('SELECT * FROM voiture WHERE id_voiture = ?', (car_id,))
        voiture = cursor.fetchone()
        conn.close()
        return render_template('edit_car.html', voiture=voiture)

@app.route('/delete_car/<int:car_id>')
def delete_car(car_id):
    conn = sql.connect("Location.db")
    cursor = conn.cursor()
    cursor.execute('DELETE FROM voiture WHERE id_voiture = ?', (car_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('Dashboard_Manager'))

@app.route('/login_manager', methods=["GET", "POST"])
def login_manager():
    if request.method == "POST":
        email = request.form["email"]
        motdepasse = request.form["motdepasse"]
        conn = sql.connect("Location.db")
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM manager WHERE email = ? AND PSWD = ?', (email, motdepasse))
        manager = cursor.fetchone()
        if manager:
            session["manager_id"] = manager["id_manager"]
            return redirect(url_for('Dashboard_Manager'))
        else:
            flash("Erreur d'authentification. Vérifiez vos identifiants.")
    return render_template("Login_Manager.html")

@app.route('/logout_manager')
def logout_manager():
    session.pop("manager_id", None)
    return redirect(url_for('login_manager'))

@app.route("/reserve", methods=["POST"])
def reserve():
    nom = request.form["nom"]
    prenom = request.form["prenom"]
    email = request.form["email"]
    telephone = request.form["telephone"]
    voiture_id = request.form["voiture_id"]
    date_debut = request.form["date_debut"]
    date_fin = request.form["date_fin"]
    
    # Validation des dates
    try:
        date_debut = datetime.strptime(date_debut, "%Y-%m-%d")
        date_fin = datetime.strptime(date_fin, "%Y-%m-%d")
        if date_debut > date_fin:
            raise ValueError("La date de début ne peut pas être après la date de fin.")
    except ValueError as e:
        flash(f"Erreur de date: {e}")
        return redirect(url_for('index'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Vérifier si la voiture est disponible
    cursor.execute('SELECT * FROM voiture WHERE id_voiture = ? AND disponibilite = "1"', (voiture_id,))
    voiture = cursor.fetchone()
    
    if not voiture:
        flash("La voiture n'est pas disponible pour la réservation.")
        conn.close()
        return redirect(url_for('index'))
    
    # Insérer la réservation
    cursor.execute('INSERT INTO reservations (nom, prenom, email, telephone, voiture_id, date_debut, date_fin, id_client, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                   (nom, prenom, email, telephone, voiture_id, date_debut, date_fin, 1, 'pending'))
    # Mettre à jour la disponibilité de la voiture
    cursor.execute('UPDATE voiture SET disponibilite = "0" WHERE id_voiture = ?', (voiture_id,))
    conn.commit()
    conn.close()
    
    flash("Réservation réussie!")
    return redirect(url_for('index'))

@app.route('/reservations')
def view_reservations():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM reservations')
    reservations = cursor.fetchall()
    conn.close()
    return render_template('reservations.html', reservations=reservations)

@app.route('/update_reservation_status/<int:reservation_id>', methods=["POST"])
def update_reservation_status(reservation_id):
    status = request.form["status"]
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE reservations SET status = ? WHERE id = ?', (status, reservation_id))
    if status == 'cancelled':
        cursor.execute('SELECT voiture_id FROM reservations WHERE id = ?', (reservation_id,))
        voiture_id = cursor.fetchone()['voiture_id']
        cursor.execute('UPDATE voiture SET disponibilite = "1" WHERE id_voiture = ?', (voiture_id,))
    conn.commit()
    conn.close()
    flash("Statut de la réservation mis à jour.")
    return redirect(url_for('view_reservations'))

if __name__ == "__main__":
    app.run(debug=True)
