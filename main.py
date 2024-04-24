class UserManager:
    def __init__(self, connection):
        self.__connection = connection
        
    @property
    def connection(self):
        return self.__connection

    @connection.setter
    def connection(self, connection):
        self.__connection = connection

    def register_user(self, firstname, lastname, username, email, password):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM user WHERE username = %s OR email = %s", (username, email))
            existing_user = cursor.fetchone()
            if existing_user:
                print("L'utilisateur existe déjà.")
                return False
            else:
                cursor.execute("INSERT INTO user (firstname, lastname, username, email, password) VALUES (%s, %s, %s, %s, %s)", (firstname, lastname, username, email, password))
                self.connection.commit()
                print("Inscription réussie.")
                return True

    def login_user(self, username, password):
        with self.connection.cursor() as cursor:
            cursor.execute('SELECT * FROM user WHERE username=%s AND password=%s', (username, password))
            user_data = cursor.fetchone()
            if user_data:
                print("Connexion réussie.")
                return User(user_data['firstname'], user_data['lastname'], username, password, user_data['email'], self.connection)
            else:
                print("Nom d'utilisateur ou mot de passe incorrect.")
                return None
    
    def update_user(self, username, new_firstname, new_lastname, new_username, new_email, new_password):
        with self.connection.cursor() as cursor:
            cursor.execute("UPDATE user SET firstname=%s, lastname=%s, username=%s, email=%s, password=%s WHERE username=%s", (new_firstname, new_lastname, new_username, new_email, new_password, username))
            self.connection.commit()
            print("Informations utilisateur mises à jour.")

    def delete_account(self, username):
        with self.connection.cursor() as cursor:
            cursor.execute("DELETE FROM user WHERE username=%s", (username,))
            self.connection.commit()
            print("Compte utilisateur supprimé.")

    def display_user_budgets(self, username):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT budget.category, budget.amount FROM budget INNER JOIN user ON budget.user_id = user.user_id WHERE user.username = %s", (username,))
            budgets = cursor.fetchall()
            if budgets:
                print("Budgets de l'utilisateur", username)
                for budget in budgets:
                    print("Catégorie:", budget['category'])
                    print("Montant:", budget['amount'])
            else:
                print("Aucun budget trouvé pour l'utilisateur", username)

    def display_user_transactions(self, username):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT transaction.date, transaction.description, transaction.amount, transaction.category FROM transaction INNER JOIN user ON transaction.user_id = user.user_id WHERE user.username = %s", (username,))
            transactions = cursor.fetchall()
            if transactions:
                print("Transactions de l'utilisateur", username)
                for transaction in transactions:
                    print("Date:", transaction['date'])
                    print("Description:", transaction['description'])
                    print("Montant:", transaction['amount'])
                    print("Catégorie:", transaction['category'])
            else:
                print("Aucune transaction trouvée pour l'utilisateur", username)


class User:
    def __init__(self, firstname, lastname, username, password, email, connection):
        self.__firstname = firstname
        self.__lastname = lastname
        self.__username = username
        self.__password = password
        self.__email = email
        self.__connection = connection
    
    @property
    def firstname(self):
        return self.__firstname
    
    @firstname.setter
    def firstname(self, firstname):
        self.__firstname = firstname
    
    @property
    def lastname(self):
        return self.__lastname
    
    @lastname.setter
    def lastname(self, lastname):
        self.__lastname = lastname
        
    @property
    def username(self):
        return self.__username
    
    @username.setter
    def username(self, username):
        self.__username = username
    
    @property
    def password(self):
        return self.__password
    
    @password.setter
    def password(self, password):
        self.__password = password
    
    @property
    def email(self):
        return self.__email
    
    @email.setter
    def email(self, email):
        self.__email = email
    
    def add_budget(self, username, category, amount_B):
        if amount_B <= 0:
            print("Le budget doit être supérieur à zéro.")
            return
    
        with self.__connection.cursor() as cursor:
            cursor.execute("SELECT * FROM user WHERE username = %s", (username,))
            existing_user = cursor.fetchone()
        
            if existing_user:
                cursor.execute("INSERT INTO budget (user_id, category, amount) VALUES (%s, %s, %s)", (existing_user['user_id'], category, amount_B))
                self.__connection.commit()
                print("Budget ajouté avec succès.")
            else:
                print("Utilisateur inexistant.")
                return
        
    def add_transaction(self, username, description, amount_T, amount_B, category):
        if amount_T <= 0:
            print("Le montant de la transaction doit être supérieur à zéro.")
            return

        with self.__connection.cursor() as cursor:
            cursor.execute("SELECT * FROM user WHERE username = %s", (username,))
            existing_user = cursor.fetchone()

            if not existing_user:
                print("Utilisateur inexistant.")
                return

            cursor.execute("SELECT * FROM budget WHERE category = %s AND user_id = %s", (category, existing_user['user_id']))
            budget = cursor.fetchone()

            if not budget:
                print("Budget non défini pour cette catégorie.")
                return

            remaining_balance = budget['amount'] - amount_T
            
            if remaining_balance < 0:
                print("Le montant de la transaction dépasse le solde disponible.")
                return

            cursor.execute("INSERT INTO transaction (user_id, description, amount, category) VALUES (%s, %s, %s, %s)", (existing_user['user_id'], description, amount_T, category))
            self.__connection.commit()

            print("Transaction ajoutée avec succès.")
    
    def update_budget(self, username, category, new_amount):
        with self.__connection.cursor() as cursor:
            cursor.execute("SELECT * FROM user WHERE username = %s", (username,))
            existing_user = cursor.fetchone()

            if not existing_user:
                print("Utilisateur inexistant.")
                return

            cursor.execute("UPDATE budget SET amount = %s WHERE user_id = %s AND category = %s", (new_amount, existing_user['user_id'], category))
            self.__connection.commit()
            print("Budget mis à jour avec succès.")

    def delete_budget(self, username, category):
        with self.__connection.cursor() as cursor:
            cursor.execute("SELECT * FROM user WHERE username = %s", (username,))
            existing_user = cursor.fetchone()

            if not existing_user:
                print("Utilisateur inexistant.")
                return

            cursor.execute("DELETE FROM budget WHERE user_id = %s AND category = %s", (existing_user['user_id'], category))
            self.__connection.commit()
            print("Budget supprimé avec succès.")

    def update_transaction(self, username, transaction_id, new_description, new_amount):
        with self.__connection.cursor() as cursor:
            cursor.execute("SELECT * FROM user WHERE username = %s", (username,))
            existing_user = cursor.fetchone()

            if not existing_user:
                print("Utilisateur inexistant.")
                return

            cursor.execute("UPDATE transaction SET description = %s, amount = %s WHERE user_id = %s AND transaction_id = %s", (new_description, new_amount, existing_user['user_id'], transaction_id))
            self.__connection.commit()
            print("Transaction mise à jour avec succès.")

    def delete_transaction(self, username, transaction_id):
        with self.__connection.cursor() as cursor:
            cursor.execute("SELECT * FROM user WHERE username = %s", (username,))
            existing_user = cursor.fetchone()

            if not existing_user:
                print("Utilisateur inexistant.")
                return

            cursor.execute("DELETE FROM transaction WHERE user_id = %s AND transaction_id = %s", (existing_user['user_id'], transaction_id))
            self.__connection.commit()
            print("Transaction supprimée avec succès.")
    
    def tax_calculation(self, username, amount_B, category):
        with self.__connection.cursor() as cursor:
        
            cursor.execute("SELECT * FROM user WHERE username = %s", (username,))
            existing_user = cursor.fetchone()
        
            if not existing_user:
                print("Utilisateur inexistant.")
                return

        
            cursor.execute("SELECT * FROM budget WHERE category = %s AND user_id = %s", (category, existing_user['user_id']))
            budget = cursor.fetchone()

            if not budget:
                print("Budget non défini pour cette catégorie.")
                return

    
            revenu_annuel = budget['amount_B'] * 12
    
            tranches = [(0, 0, 0.0), (3000, 0, 0.08), (5000, 120, 0.22), (10000, 620, 0.32), (20000, 1620, 0.37), (35000, 3620, 0.45)]

    
            impot = 0
            for i in range(len(tranches)):
                if revenu_annuel <= tranches[i][0]:
                    impot += (revenu_annuel - tranches[i][1]) * tranches[i][2]
                    break
                else:
                    impot += (tranches[i][0] - tranches[i][1]) * tranches[i][2]

            return impot
        
        

class Budget:
    def __init__(self, category, amount_T):
        self.category = category
        self.amount_T = amount_T

class Transaction:
    def __init__(self, description, amount_B, category):
        self.description = description
        self.amount_B = amount_B
        self.category = category
        

    @property
    def description(self):
        return self.__description
    
    @description.setter
    def description(self, description):
        self.__description = description
    
    @property
    def amount_B(self):
        return self.__amount_B
    
    @amount_B.setter
    def amount_B(self, amount_B):
        self.__amount_B = amount_B
    
    @property
    def category(self):
        return self.__category
    
    @category.setter
    def category(self, category):
        self.__category = category
    