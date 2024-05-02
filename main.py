class UserManager:
    def __init__(self, connection):
        self.connection = connection

    def register_user(self, firstname, lastname, username, email, password):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE username = %s OR email = %s", (username, email))
            existing_user = cursor.fetchone()
            if existing_user:
                return False
            else:
                cursor.execute(
                    "INSERT INTO users (firstname, lastname, username, email, password) VALUES (%s, %s, %s, %s, %s)",
                    (firstname, lastname, username, email, password)
                )
                if cursor.rowcount > 0:
                    self.connection.commit()
                    return True
                else:
                    return False

    def login_user(self, username, password):
        with self.connection.cursor() as cursor:
            cursor.execute('SELECT * FROM users WHERE username=%s AND password=%s', (username, password))
            user_data = cursor.fetchone()
            if user_data:
                return User(user_data[1], user_data[2], username, password, user_data[3], self.connection)
            else:
                return None

    def update_user(self, username, old_password, new_firstname, new_lastname, new_email, new_password):
        with self.connection.cursor() as cursor:
            cursor.execute(
                "UPDATE users SET firstname=%s, lastname=%s, email=%s, password=%s WHERE username=%s AND password=%s",
                (new_firstname, new_lastname, new_email, new_password, username, old_password)
            )
            if cursor.rowcount > 0:
                self.connection.commit()
                return True
            else:
                return False

    def delete_account(self, username, password):
        with self.connection.cursor() as cursor:
            cursor.execute("DELETE FROM users WHERE username=%s AND password=%s", (username, password))
            if cursor.rowcount > 0:
                self.connection.commit()
                return True
            else:
                return False

    def get_firstname_lastname(self, username):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT firstname, lastname FROM users WHERE username = %s", (username,))
            row = cursor.fetchone()
            if row:
                firstname, lastname = row
                return f"{firstname} {lastname}"
            else:
                return None

    def get_budgets(self, username):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM budgets WHERE username = %s", (username,))
            budgets = cursor.fetchall()

            if not budgets:
                return None
            
            budget_list = []
            for budget in budgets:
                budget_id = budget[0]
                amount = budget[2]
                category = budget[3]
                date_b = budget[4]
                budget_list.append(f"{budget_id}  {amount}  {category}  {date_b}")

            return "\n".join(budget_list)

    def get_transactions(self, username):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM transactions WHERE username = %s", (username,))
            transactions = cursor.fetchall()

            if not transactions:
                return None

            transaction_list = []
            for transaction in transactions:
                transaction_id = transaction[0]
                amount = transaction[3]
                category = transaction[4]
                date_Tran = transaction[5]
                transaction_list.append(f"{transaction_id}  {amount}  {category}  {date_Tran}")

            return "\n".join(transaction_list)

    def get_total_budget(self, username):
        with self.connection.cursor() as cursor:
            # If SUM(amount_B) return null then 0
            cursor.execute("SELECT COALESCE(SUM(amount_B), 0) FROM budgets WHERE username = %s", (username,))
            total_budget_result = cursor.fetchone()[0]
            return total_budget_result

    def get_sorted_transactions_and_budgets_matrix(self, username):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                (SELECT 'transaction' AS type, transaction_id, amount_T, category, date_Tran 
                FROM transactions 
                WHERE username = %s)
                UNION
                (SELECT 'budget' AS type, budget_id, amount_B, category, date_b 
                FROM budgets 
                WHERE username = %s) ORDER BY date_Tran""",
                (username, username)
            )
            
            transactions_and_budgets = cursor.fetchall()
            
            if not transactions_and_budgets:
                return None
            
            result_matrix = []
            for item in transactions_and_budgets:
                if item[0] == 'transaction':
                    transaction_id = item[1]
                    ttype = "transaction"
                    amount = item[2]
                    category = item[3]
                    date_Tran = item[4]
                    result_matrix.append([transaction_id, ttype, amount, category, date_Tran])
                elif item[0] == 'budget':
                    budget_id = item[1]
                    ttype = "budget"
                    amount = item[2]
                    category = item[3]
                    date_b = item[4]
                    result_matrix.append([budget_id, ttype, amount, category, date_b])

            return result_matrix

    def get_sorted_transactions_and_budgets(self, username):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                (SELECT 'transaction' AS type, transaction_id, amount_T, category, date_Tran 
                FROM transactions 
                WHERE username = %s)
                UNION
                (SELECT 'budget' AS type, budget_id, amount_B, category, date_b 
                FROM budgets 
                WHERE username = %s) ORDER BY date_Tran""",
                (username, username)
            )
            
            transactions_and_budgets = cursor.fetchall()
            if transactions_and_budgets:
                result_list = []
                for item in transactions_and_budgets:
                    if item[0] == 'transaction':
                        transaction_id = item[1]
                        amount = item[2]
                        category = item[3]
                        date_Tran = item[4]
                        result_list.append(f"{transaction_id}  {amount}  {category}  {date_Tran}")
                    elif item[0] == 'budget':
                        budget_id = item[1]
                        amount = item[2]
                        category = item[3]
                        date_b = item[4]
                        result_list.append(f"{budget_id}  {amount}  {category}  {date_b}")

                return "\n".join(result_list)
            else:
                print("Aucune transaction ni budget trouvé pour cet utilisateur.")
                return None

    def get_total_transactions(self, username):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT COALESCE(SUM(amount_T), 0) FROM transactions WHERE username = %s", (username,))
            total_transactions_result = cursor.fetchone()[0]
            return total_transactions_result

    def get_balance(self, username):
        total_budget = self.get_total_budget(username)
        total_transactions = self.get_total_transactions(username)

        balance = total_budget - total_transactions
        return balance
    

class User:
    def __init__(self, firstname, lastname, username, password, email, connection):
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.password = password
        self.email = email
        self.connection = connection

    def add_budget(self, category, amount_B):
        with self.connection.cursor() as cursor:
            cursor.execute("INSERT INTO budgets (username, category, amount_B) VALUES (%s, %s, %s)",
                           (self.username, category, amount_B))
            self.connection.commit()
            print("Budget ajouté avec succès.")

    def add_transaction(self, amount_T, category):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT COALESCE(amount_B, 0) FROM budgets WHERE username = %s AND category = %s", (self.username, category))
            budget = cursor.fetchone()[0]
            if budget >= amount_T:
                cursor.execute("INSERT INTO transactions (username, amount_T, category) VALUES (%s, %s, %s)",
                               (self.username, amount_T, category))
                self.connection.commit()
                print("Transaction ajoutée avec succès.")
            else:
                print("Le montant de la transaction dépasse le solde disponible pour cette catégorie.")

    def update_transaction(self, transaction_id, new_amount, new_category):
        with self.connection.cursor() as cursor:
            cursor.execute("UPDATE transactions SET category=%s, amount_T=%s WHERE username=%s AND transaction_id=%s",
                           (new_category, new_amount, self.username, transaction_id))
            self.connection.commit()
            print("Transaction mise à jour avec succès.")

    def delete_transaction(self, transaction_id):
        with self.connection.cursor() as cursor:
            cursor.execute("DELETE FROM transactions WHERE username=%s AND transaction_id=%s",
                           (self.username, transaction_id))
            self.connection.commit()
            print("Transaction supprimée avec succès.")
