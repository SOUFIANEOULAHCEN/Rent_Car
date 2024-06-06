import sqlite3 as sql


# ----------------------CLASS ADMIN-------------------------------
class Administrateur:
    def __init__(self, nom, prenom, email, mot_de_passe):
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.mot_de_passe = mot_de_passe

    def get_nom(self):
        return self.nom

    def set_nom(self, nom):
        self.nom = nom

    def get_prenom(self):
        return self.prenom

    def set_prenom(self, prenom):
        self.prenom = prenom

    def get_email(self):
        return self.email

    def set_email(self, email):
        self.email = email

    def get_mot_de_passe(self):
        return self.mot_de_passe

    def set_mot_de_passe(self, mot_de_passe):
        self.mot_de_passe = mot_de_passe
        
        
    @staticmethod
    def get_idAdmin(Administrateur):
        try:
            connexion = sql.connect('Location.db')
            cusrsor = connexion.cursor()
            
            cusrsor.execute('''SELECT id_admin FROM administrateur WHERE nom = ? AND prenom =? AND email = ? and PSWD = ?''',
                            (Administrateur.get_nom() , Administrateur.get_prenom() , Administrateur.get_email() , Administrateur.get_mot_de_passe()))
            id_admin = cusrsor.fetchone()
            if id_admin :
                return id_admin[0]
        except sql.Error as e :
            print(f'Erreur :{e}')
        finally:
            if connexion :
                connexion.commit()
                connexion.close()
    @staticmethod
    def Add_Admin(Administrateur) :
        nom = Administrateur.get_nom()
        prenom = Administrateur.get_prenom()
        email = Administrateur.get_email()
        PSWD = Administrateur.get_mot_de_passe()
        try:
            connexion = sql.connect('Location.db')
            cursor = connexion.cursor()
            cursor.execute(''' INSERT INTO administrateur (nom , prenom , email , PSWD) VALUES (?,?,?,?)''',
                           (nom , prenom , email , PSWD))
        except sql.Error as e :
            print(f'Erreur : {e}')
        finally:
            if  connexion :
                connexion.commit()
                connexion.close()
        
    @staticmethod
    def get_managers(idAdmin):
        try:
            connexion = sql.connect('Location.db')
            cusrsor = connexion.cursor()
    
            cusrsor.execute('''SELECT * FROM manager WHERE id_admin = ?''',(idAdmin,))
            data = cusrsor.fetchall()
            return data
        except sql.Error as e:
            print(f'Erreur de connection {e}')
        finally:
            connexion.commit()
            connexion.close()

        
    @staticmethod
    def add_manager(Manager , idAdmin):
        
        try:
            connexion = sql.connect('Location.db')
            cursor = connexion.cursor()
            cursor.execute('''INSERT INTO manager (nom ,prenom , email , PSWD , id_admin ) VALUES(?,?,?,?,?)'''
                           ,(Manager.get_nom() , Manager.get_prenom() , Manager.get_email() , Manager.get_PSWD(), idAdmin)  )
        except sql.Error as e :
            print(f'erreur :{e}')
        finally:
            if connexion :
                connexion.commit()
                connexion.close()
                
    @staticmethod
    def delete_manager(idManager ,  idAdmin):
        try:
            connexion = sql.connect('Location.db')
            cursor = connexion.cursor()
            cursor.execute(''' DELETE FROM manager WHERE id_manager = ? AND id_admin = ?''' , (idManager , idAdmin) )
        except sql.Error as e :
            print(f'erreur :{e}')
        finally:
            if connexion :
                connexion.commit()
                connexion.close()    
    
    
#... (other code)

# Instantiate the newManager1 object
# admin = Administrateur('Soufiane' , 'oulahcen' , 'soufiane@gmail.com' , 'Admin123')
# # Administrateur.Add_Admin(admin) #correct
# idAdmin = Administrateur.get_idAdmin(admin)#correct
# # manager1 = manager('simido' , 'bouih' , 'simido@gmail.com' , 'manager123')
# # Administrateur.add_manager(manager1,idAdmin)
# newManager1 = manager('toni', 'kros', 'toni@gmail.com', 'manager123')

# idAdmin = Administrateur.get_idAdmin(admin)#correct
# Administrateur.get_managers(idAdmin)

# admin.add_manager(newManager1 ,idAdmin)#correct
# # admin.delete_manager(idAdmin , manager1) 


#------------------ CLASS MANAGER---------------------------------------


class manager:
    def __init__(self, nom, prenom, email, PSWD):
        # self.idManager = idManager
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.PSWD = PSWD

    # Getter for idManager
    # def get_idManager(self):
    #     return self.idManager

    # # Setter for idManager
    # def set_idManager(self, idManager):
    #     self.idManager = idManager

    # Getter for nom
    def get_nom(self):
        return self.nom

    # Setter for nom
    def set_nom(self, nom):
        self.nom = nom

    # Getter for prenom
    def get_prenom(self):
        return self.prenom

    # Setter for prenom
    def set_prenom(self, prenom):
        self.prenom = prenom

    # Getter for email
    def get_email(self):
        return self.email

    # Setter for email
    def set_email(self, email):
        self.email = email

    # Getter for PSWD
    def get_PSWD(self):
        return self.PSWD

    # Setter for PSWD
    def set_PSWD(self, PSWD):
        self.PSWD = PSWD

    @staticmethod
    def add_manager(manager):
        try:
            connexion = sql.connect("Location.db")
            cursor = connexion.cursor()
            cursor.execute(
                """INSERT INTO manager (nom , prenom ,email ,PSWD) VALUES (?,?,?,?)""",
                (
                    manager.get_nom(),
                    manager.get_prenom(),
                    manager.get_email(),
                    manager.get_PSWD(),
                ),
            )
        except sql.Error as e:
            print(f"erreur : {e}")
        finally:
            if connexion:
                connexion.commit()
                connexion.close()

    @staticmethod
    def get_idManager(manager):#worked
        nom = manager.get_nom()
        prenom = manager.get_prenom()
        try:
            connexion = sql.connect("Location.db")
            cursor = connexion.cursor()
            cursor.execute(
                "SELECT id_manager FROM manager WHERE nom = ? AND prenom = ?",
                (nom, prenom),
            )
            row = cursor.fetchone()
            if row:
                return row[0]
            else:
                print("Manager non trouvé.")
                return None
        except sql.Error as e:
            print("Erreur lors de la récupération de l'ID du manager:", e)
        finally:
            if connexion:
                connexion.commit()
                connexion.close()
                
    @staticmethod
    def get_cars(idManager):#worked
        try:
            connexion = sql.connect("Location.db")
            connexion.row_factory = sql.Row  
            cursor = connexion.cursor()
            cursor.execute(""" SELECT rowid,* FROM voiture WHERE id_manager = ?""", (idManager,))
            cars = cursor.fetchall()
            # cars = []
            # id =1
            # for row in data:
            #     # cars.append(dict(row))
            #     print(f'{id}: marque :{row[1]} ,modele :  {row[2]} ,immatriculation : {row[3]} ,categorie : {row[4]} ,prix : {row[5]}') 
            #     id+=1
            # return cars
            return cars
        except sql.Error as e:
            print("Erreur lors de la récupération des voitures:", e)
            return []  # Return an empty list if there's an error
        finally:
            if connexion:
                connexion.commit()
                connexion.close()


    @staticmethod
    def add_car(Voiture, idManager):
        # idv = Voiture.get_idv(Voiture)
        marque = Voiture.get_marque()
        modele = Voiture.get_modele()
        immatricule = Voiture.get_immatricule()
        categorie = Voiture.get_categorie()
        prix = Voiture.get_prix()
        disponible = Voiture.is_disponible()
        path = Voiture.get_path()

        connexion = sql.connect("Location.db")
        cursor = connexion.cursor()

        cursor.execute(
            """INSERT INTO voiture (marque, modele, immatriculation, categorie, prix,disponibilite, id_manager , path)
                         VALUES (?, ?, ?, ?, ?, ?, ?,?)""",
            ( marque, modele, immatricule, categorie, prix, disponible, idManager,path),
        )
        connexion.commit()
        connexion.close() #worked

    @staticmethod
    def delete_car(Voiture, idManager):
        idv = Voiture.get_idv(Voiture)
        connexion = sql.connect("Location.db")
        cursor = connexion.cursor()

        cursor.execute(
            """DELETE FROM voiture WHERE id_voiture =? and id_manager = ?""",
            (idv, idManager),
        )
        connexion.commit()
        connexion.close() #worked


# Instantiate multiple Voiture objects representing different cars
# car1 = Voiture("volvo", "Corolla", "ABC123", "Compact", 50, True , 'images/VOLVO.png')
# car2 = Voiture("kia", "Mustang", "XYZ456", "Sports", 100, True , 'images/kia ceed.png')
# car3 = Voiture("VOLKSWAGEN", "Civic", "DEF789", "Compact", 60, True , 'images/VOLKSWAGEN.png')
# car4 = Voiture("R4", "Civic", "AZF589", "Compact", 10, True , 'images/BMW.png')
# car5 = Voiture("R12", "Civic", "AZF589", "Compact", 15, True , 'images/BMW.png')
# /static
# manager1 = manager("toni", "kros", "toni@gmail.com", "manager123")
# manager_id1 = manager.get_idManager(manager1)
# manager.add_manager(manager1)


# manager.add_car(car1, manager_id1)
# manager.add_car(car2, manager_id1)
# manager.add_car(car3, manager_id1)
# manager.add_car(car4, manager_id1)
# manager.add_car(car5, manager_id1)
# manager.get_cars(manager_id1)
# manager.delete_car(car5 , manager_id1)
# manager.delete_car(car1 , manager_id1)
# manager.delete_car(car2 , manager_id1)
# manager.delete_car(car3 , manager_id1)
# manager.delete_car(car4 , manager_id1)

# print(manager.get_cars(manager_id1))





# manager2.add_car(car1, manager_id)

# # Display all cars currently in the database
# idmanager1 = manager.get_idManager(manager1)
# manager.get_cars(idmanager1)
# manager2.get_cars()



# # Call the delete_car() method to delete the specified car
# manager2.delete_car(car1, manager2.get_idManager(manager2.get_nom() , manager2.get_prenom()))

# # Display all cars again to verify whether the car was deleted
# manager.get_cars(manager1.get_idManager(manager1))

# manager_id = manager.get_idManager(manager1)

#delete cars :

# manager.delete_car(car2 , manager_id1)
# manager.delete_car(car3 , manager_id1)

        
          
          
          
          
# -------------------------CLASS VOITURE ----------------------------6

class Voiture:
    def __init__(
        self, marque, modele, immatricule, categorie, prix ,  disponibilite=True, path=''
    ):
        # self.idv = idV
        self.marque = marque
        self.modele = modele
        self.immatricule = immatricule
        self.categorie = categorie
        self.prix = prix
        self.disponible = disponibilite
        self.path = path


    # # Setter for idv
    # def set_idv(self, idv):
    #     self.idv = idv

    # Getter for marque
    def get_marque(self):
        return self.marque

    # Setter for marque
    def set_marque(self, marque):
        self.marque = marque

    # Getter for modele
    def get_modele(self):
        return self.modele

    # Setter for modele
    def set_modele(self, modele):
        self.modele = modele

    # Getter for immatricule
    def get_immatricule(self):
        return self.immatricule

    # Setter for immatricule
    def set_immatricule(self, immatricule):
        self.immatricule = immatricule

    # Getter for categorie
    def get_categorie(self):
        return self.categorie

    # Setter for categorie
    def set_categorie(self, categorie):
        self.categorie = categorie

    # Getter for prix
    def get_prix(self):
        return self.prix

    # Setter for prix
    def set_prix(self, prix):
        self.prix = prix

    def get_path(self):
        return self.path

    # Setter for marque
    def set_path(self, path):
        self.path = path
        
    # Getter for disponibilite
    def is_disponible(self):
        return self.disponible

    # Setter for disponibilite
    def set_disponible(self, disponibilite):
        self.disponible = disponibilite

    def get_details(self):
        return f" Marque: {self.marque}, Modele: {self.modele}, Immatricule: {self.immatricule}, Categorie: {self.categorie}, Prix: {self.prix}, Disponible: {self.disponible}"

    def reserve(self):
        return self.set_disponible(False)

    def annuler_reservation(self):
        return self.set_disponible(True)

        # Getter for idv

    @staticmethod
    def get_idv(Voiture):
        try:
            connexion = sql.connect("Location.db")
            cursor = connexion.cursor()
            cursor.execute(
                """SELECT id_voiture FROM voiture WHERE marque=? AND modele=? AND immatriculation=? AND categorie=? AND path=?""",
                (
                    Voiture.marque,
                    Voiture.modele,
                    Voiture.immatricule,
                    Voiture.categorie,
                    Voiture.path,
                ),
            )
            idVoiture = cursor.fetchone()
            if idVoiture:
                return idVoiture[0]
            else:
                print("Aucune voiture correspondante trouvée.")
                return None
        except sql.Error as e:
            print("Erreur:", e)
        finally:
            if connexion:
                connexion.commit()
                connexion.close()


# voiture_test = Voiture("Ford", "Mustang", "XYZ456", "Sports", 100,)

# Obtenir l'ID de la voiture
# id_voiture = Voiture.get_idv(voiture_test)
# print("ID de la voiture:", id_voiture)

        

# ----------------------CLASS CLIENT ---------------------------6


class client:
    def __init__(self, nom, prenom, email, telephone):
        # self.idClient = idClient
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.telephone = telephone

    # # Getter for idClient
    # def get_idClient(self):
    #     return self.idClient

    # # Setter for idClient
    # def set_idClient(self, idClient):
    #     self.idClient = idClient

    # Getter for nom
    def get_nom(self):
        return self.nom

    # Setter for nom
    def set_nom(self, nom):
        self.nom = nom

    # Getter for prenom
    def get_prenom(self):
        return self.prenom

    # Setter for prenom
    def set_prenom(self, prenom):
        self.prenom = prenom

    # Getter for email
    def get_email(self):
        return self.email

    # Setter for email
    def set_email(self, email):
        self.email = email

    # Getter for telephone
    def get_telephone(self):
        return self.telephone

    # Setter for telephone
    def set_telephone(self, telephone):
        self.telephone = telephone
        
    
    @staticmethod
    def get_idC(client):
        nom = client.get_nom()
        prenom = client.get_prenom()
        email = client.get_email()
        telephone = client.get_telephone()
        
        try:
            connexion = sql.connect('Location.db')
            cursor = connexion.cursor()
            cursor.execute('''SELECT id_client FROM client where nom = ? AND prenom = ? AND email = ? AND telephone = ?''',
                           (nom , prenom , email , telephone))
            id_client = cursor.fetchone()
            if id_client:
                return id_client[0]
        except sql.Error as e :
            print(f'erreur : {e}')
        finally:
            if connexion :
                connexion.commit()
                connexion.close()
        
        
    @staticmethod
    def ajouter_client(client):
        nom = client.get_nom()
        prenom = client.get_prenom()
        email = client.get_email()
        telephone = client.get_telephone()

        try:
            connexion = sql.connect("Location.db")
            connexion.row_factory = sql.Row
            cursor = connexion.cursor()
            
            cursor.execute(
                """ INSERT INTO client (nom , prenom , email ,telephone)  VALUES(?,?,?,?)""",
                (nom, prenom, email, telephone),
            )
        except sql.Error as e:
            print("Error:", e)
        finally:
            if connexion:
                connexion.commit()
                connexion.close()

    @staticmethod
    def get_reservations(idClient):
        try:
            connexion = sql.connect("Location.db")
            connexion.row_factory = sql.Row
            cursor = connexion.cursor()
            
            # select name of client
            cursor.execute(
                """SELECT nom, prenom FROM client WHERE id_client = ?""", (idClient,)
            )
            nomClient = cursor.fetchall()
            if nomClient:
                print(f"Client: {nomClient[0]['nom']} {nomClient[0]['prenom']}")
    
                cursor.execute(
                    """SELECT * FROM voiture WHERE id_client = ? AND disponibilite = ?""",
                    (idClient, False),
                )
                data = cursor.fetchall()
                print("Number of reservations found:", len(data))  # Debugging output
                for row in data:
                    print(
                        f"Marque: {row['marque']}, Modele: {row['modele']}, Immatricule: {row['immatriculation']}, Categorie: {row['categorie']}, Prix: {row['prix']}"
                    )
            else:
                print("Client non trouvé.")
        except sql.Error as e:
            print("Error:", e)
        finally:
            if connexion:
                connexion.commit()
                connexion.close()
                



    @staticmethod
    def reserver_voiture(idClient, idVoiture):
        try:
            connexion = sql.connect("Location.db")
            cursor = connexion.cursor()

            # checking if the car is available or not
            cursor.execute(
                """SELECT * FROM voiture WHERE id_voiture = ? AND disponibilite = ?""",
                (idVoiture, True),
            )

            car = cursor.fetchone()

            if car:
                cursor.execute(
                    """UPDATE voiture SET disponibilite = ? , id_client = ? WHERE id_voiture = ?""",
                    (False, idClient, idVoiture),
                )
                print("La voiture reserver  avec succes !")
            else:
                print("La voiture n'est  pas disponible")
        except sql.Error as e:
            print("Error:", e)
        finally:
            if connexion:
                connexion.commit()
                connexion.close()

    @staticmethod
    def annuler_reservation(idClient, idVoiture):
        try:
            connexion = sql.connect("Location.db")
            cursor = connexion.cursor()

            cursor.execute(
                """SELECT * FROM voiture WHERE id_voiture = ? AND id_client = ?""",
                (idVoiture, idClient),
            )

            reserved_car = cursor.fetchone()

            if reserved_car:
                cursor.execute(
                    """UPDATE voiture SET disponibilite = ? , id_client = ? WHERE id_voiture = ?""",
                    (True, None, idVoiture)
                )
                print("La reservation est annuler")
            else:
                print("Vous n'avez pas réservé cette voiture.")
        except sql.Error as e:
            print("Error:", e)
        finally:
            if connexion:
                connexion.commit()
                connexion.close()


# client.get_reservations(1)
# client1 = client('toni','Kroos','kroos@gmail.com','065478932')
# client.ajouter_client(client1)
# idC = client.get_idC(client1)
# client.reserver_voiture(idC, 5) 
# client.annuler_reservation(idC,5) 
# client.get_reservations(idC)



# --------------------------------------------------------------------------------------
# admin = Administrateur('Soufiane' , 'oulahcen' , 'soufiane@gmail.com' , 'Admin123')
# idAdmin = Administrateur.get_idAdmin(admin)#correct
# newManager1 = manager('toni', 'kros', 'toni@gmail.com', 'manager123')
# # add_manager(Manager , idAdmin):
# # Administrateur.add_manager(newManager1 ,idAdmin)

admin = Administrateur("Oulahcen", "Soufiane", "soufiane@gmail.com", "motdepasse123")
# Administrateur.Add_Admin(admin)
# newManager1 = manager('toni', 'kroos', 'toni@gmail.com', 'manager123')

# idAdmin = Administrateur.get_idAdmin(admin)
# Administrateur.add_manager(newManager1,idAdmin)
# print(f"idAdmin: {idAdmin}")
# managers = Administrateur.get_managers(idAdmin)
# print(f"managers: {managers}")




# car1 = Voiture("volvo", "Corolla", "ABC123", "Compact", 50, True , 'img/VOLVO.png')
# car2 = Voiture("kia", "Mustang", "XYZ456", "Sports", 100, True , 'img/kia ceed.png')
# car3 = Voiture("VOLKSWAGEN", "Civic", "DEF789", "Compact", 60, True , 'img/VOLKSWAGEN.png')
# car4 = Voiture("R4", "Civic", "AZF589", "Compact", 10, True , 'img/BMW.png')
# car5 = Voiture("R12", "Civic", "AZF589", "Compact", 15, True , 'img/BMW.png')
# /static
# manager1 = manager("toni", "kros", "toni@gmail.com", "manager123")
# manager_id1 = manager.get_idManager(newManager1)
# manager.add_manager(manager1)

# manager.add_car(car1, manager_id1)
# manager.add_car(car2, manager_id1)
# manager.add_car(car3, manager_id1)
# manager.add_car(car4, manager_id1)
# manager.add_car(car5, manager_id1)
# manager.get_cars(manager_id1)
# manager.delete_car(car5 , manager_id1)
# manager.delete_car(car1 , manager_id1)
# manager.delete_car(car2 , manager_id1)
# manager.delete_car(car3 , manager_id1)
# manager.delete_car(car4 , manager_id1)

