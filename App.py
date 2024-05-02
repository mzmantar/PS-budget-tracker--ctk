import re
import customtkinter as ctk
import customtkinter

from main import UserManager
from Connexion import CONNEXION
from CTkMessagebox import CTkMessagebox

customtkinter.set_appearance_mode("light")

def toggle_dark_mode():
    global dark_mode_variable
    if dark_mode_variable.get() == 1:
        customtkinter.set_appearance_mode("dark")
    else:
        customtkinter.set_appearance_mode("light")

def perform_update():
    global register_button,old_username, new_firstname_entry, new_lastname_entry, new_email_entry, old_password_entry, new_password_entry,dashbord_BT,update_user_window
    username = old_username.get()
    new_firstname = new_firstname_entry.get()
    new_lastname = new_lastname_entry.get()
    new_email = new_email_entry.get()
    old_password = old_password_entry.get()
    new_password = new_password_entry.get()
    
    user_manager = UserManager(CONNEXION)
    update_success = user_manager.update_user(username, old_password, new_firstname, new_lastname, new_email, new_password)
        
    if update_success:
        CTkMessagebox(title="Info", message="Félicitations, votre profil a été mis à jour avec succès.")
        update_user_window.destroy()
        deconnexion()
    else:
        CTkMessagebox(title="Erreur", message="Échec de la mise à jour du profil. Veuillez vérifier vos informations.", icon="cancel")

def update_user(username,row):
    global register_button,old_username, new_firstname_entry, new_lastname_entry, new_email_entry, old_password_entry, new_password_entry,update_user_window
    update_user_window = ctk.CTk()
    update_user_window.geometry("800x700")
    update_user_window.title("MISE À JOUR DU PROFIL - BUDGET-TRACKER")
    
    label = ctk.CTkLabel(update_user_window,font=("ariel", 20,'bold'), text="BUDGET TRACKER")
    label.pack(pady=35, padx=20)

    frame = ctk.CTkFrame(master=update_user_window)
    frame.pack(pady=15, padx=35, fill='both', expand=True)
    
    label = ctk.CTkLabel(master=frame, text=f'UPDATE-PROFIL {row.upper()}')
    label.pack(pady=12, padx=50)
    
    old_username = ctk.CTkEntry(master=frame)
    old_username.insert(0, username)
    old_username.pack(pady=12, padx=10)

    new_firstname_entry = ctk.CTkEntry(master=frame, placeholder_text="Prénom")
    new_firstname_entry.pack(pady=12, padx=10)  
    
    new_lastname_entry = ctk.CTkEntry(master=frame, placeholder_text="Nom de famille")
    new_lastname_entry.pack(pady=12, padx=10)
    
    new_email_entry = ctk.CTkEntry(master=frame, placeholder_text="Email")
    new_email_entry.pack(pady=12, padx=10)
    
    old_password_entry = ctk.CTkEntry(master=frame, placeholder_text="Ancien mot de passe", show="*")
    old_password_entry.pack(pady=12, padx=10)
    
    new_password_entry = ctk.CTkEntry(master=frame, placeholder_text="Nouveau mot de passe", show="*")
    new_password_entry.pack(pady=12, padx=10)
    
    register_button = ctk.CTkButton(master=frame, text="Mettre à jour", 
                                     command=lambda: perform_update())
    register_button.pack(pady=12, padx=10)
    
    cancel_button = ctk.CTkButton(master=frame, text='Annuler', command=update_user_window.destroy)
    cancel_button.pack(pady=12, padx=10)
    
    budget_tracker_label = ctk.CTkLabel(update_user_window, font=("", 10), text="© Budget-tracker 2024-2025 Conception et réalisation par Med-Mehdi ZMANTAR & Jassem BOUGHATAS. Tous droits réservés.")
    budget_tracker_label.pack(pady=10)
    
    update_user_window.mainloop()
    
def deconnexion():
    global dashboard_frame, login_frame, app
    dashboard_frame.pack_forget()
    app.title("PAGE DE CONNEXION - BUDGET-TRACKER")
    app.geometry("800x600")
    login_frame.pack()
    global password_entry
    password_entry.delete(0, 'end')

def login(username_entry,password_entry):
    username = username_entry.get()
    password = password_entry.get()
    
    user_manager = UserManager(CONNEXION)
    User = user_manager.login_user(username, password)
    
    if not User:
        CTkMessagebox(title="Error", message="Votre username ou mot de passe est incorrect", icon="cancel")
        return
    
    login_frame.pack_forget()

    global dashboard_frame
    dashboard_frame = ctk.CTkFrame(app, fg_color="transparent")
    dashboard_frame.pack(pady=15, padx=35, fill='both', expand=True)

    global user_id
    row = user_manager.get_firstname_lastname(username)
    budgets = user_manager.get_sorted_transactions_and_budgets(username)
    total_budge = user_manager.get_total_budget(username)
    total_transactions = user_manager.get_total_transactions(username)
    balance = user_manager.get_balance(username)

    rows =user_manager.get_sorted_transactions_and_budgets_matrix(username)

    app.geometry("1200x900")
    app.title("DASHBOARD - BUDGET-TRACKER")
    #dashbord_BT.iconbitmap("logo/badgettraker.ico")

    global dark_mode_variable

    Dec_button = ctk.CTkButton(dashboard_frame, text='DECONNEXION', command=deconnexion)
    Dec_button.pack(side='top', anchor='ne', padx=20, pady=20)
    
    user_id = ctk.CTkLabel(dashboard_frame, font=("",15), text=f"{row.upper()}", cursor="hand2")
    user_id.pack(side='top', anchor='w', padx=35, pady=20)
    user_id.bind("<Button-1>", lambda e: update_user(username,row))

    label = ctk.CTkLabel(dashboard_frame, font=("", 20, 'bold'), text='---BUDGET-TRACKER---')
    label.pack(pady=2, padx=10, fill='both')
    
    frame2 = ctk.CTkFrame(dashboard_frame)
    frame2.pack(side='right', pady=200, padx=15, fill='both')
    
    frame1 = ctk.CTkFrame(dashboard_frame)
    frame1.pack(side='left', pady=200, padx=15, fill='both')

    middle_frame = ctk.CTkFrame(dashboard_frame)
    middle_frame.pack(pady=100, padx=5, fill='both', expand=True)

    balance_label = ctk.CTkLabel(middle_frame, font=("", 28), text=f"Balance: {int(balance)}DT")
    balance_label.pack(pady=10, padx=10)

    # Rows Frame
    rows_frame = ctk.CTkScrollableFrame(middle_frame, height=100, label_font=("", 20))
    rows_frame.pack(pady=10, padx=10, fill='both', expand=True)

    id_labell = ctk.CTkLabel(rows_frame, text="ID")
    id_labell.grid(row=0, column=0, padx=20, pady=10)

    ttype_labell = ctk.CTkLabel(rows_frame, text="Type")
    ttype_labell.grid(row=0, column=1, padx=20, pady=10)

    amount_labell = ctk.CTkLabel(rows_frame, text="Montant")
    amount_labell.grid(row=0, column=2, padx=20, pady=10)

    category_labell = ctk.CTkLabel(rows_frame, text="Catégorie")
    category_labell.grid(row=0, column=3, padx=20, pady=10)

    date_labell = ctk.CTkLabel(rows_frame, text="Date")
    date_labell.grid(row=0, column=4, padx=20, pady=10)

    for i, row in enumerate(rows):
        id = row[0]
        ttype = row[1]
        amount = row[2]
        category = row[3]
        date = row[4]

        id_label = ctk.CTkLabel(rows_frame, text=f"{id}")
        id_label.grid(row=i+1, column=0, padx=20, pady=10)

        ttype_label = ctk.CTkLabel(rows_frame, text=f"{ttype}")
        ttype_label.grid(row=i+1, column=1, padx=20, pady=10)

        amount_label = ctk.CTkLabel(rows_frame, text=f"{amount}DT")
        amount_label.grid(row=i+1, column=2, padx=20, pady=10)

        category_label = ctk.CTkLabel(rows_frame, text=f"{category}")
        category_label.grid(row=i+1, column=3, padx=20, pady=10)

        date_label = ctk.CTkLabel(rows_frame, text=f"{date}")
        date_label.grid(row=i+1, column=4, padx=20, pady=10)

    select_combobox = ctk.CTkComboBox(middle_frame, values=["Budget", "Transaction"])
    select_combobox.pack(pady=10, padx=10, fill='both')

    ammount_entry = ctk.CTkEntry(middle_frame, placeholder_text="Montant")
    ammount_entry.pack(pady=10, padx=10, fill='both')

    submit_button = ctk.CTkButton(middle_frame, text="Ajouter")
    submit_button.pack(pady=10, padx=10, fill='both')
    
    dark_mode_button = ctk.CTkSwitch(dashboard_frame, onvalue=1, offvalue=0, text='Activer le mode sombre ou clair', variable=dark_mode_variable, command=toggle_dark_mode)
    dark_mode_button.pack(pady=10)

    Budjet_traker = ctk.CTkLabel(dashboard_frame, font=("", 10), text="© Budget-tracker 2024-2025 Conception et réalisation par Med-Mehdi ZMANTAR & Jassem BOUGHATAS. Tous droits réservés.")
    Budjet_traker.pack(pady=10)
    
def validate_email(email):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        CTkMessagebox(title="Error", message="Adresse email invalide!!!", icon="cancel")
        return False
    return True

def validate_registration(first_name, last_name, email, username, password):
    if not all([first_name, last_name, email, username, password]):
        CTkMessagebox(title="Error", message="Remplissez tous les champs.!!!", icon="cancel")
        return False
    if not validate_email(email):
        return False
    return True

def register():
    global first_name_entry, last_name_entry, email_entry, registration_user_entry, registration_pass_entry
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    email = email_entry.get()
    username = registration_user_entry.get()
    password = registration_pass_entry.get()

    if validate_registration(first_name, last_name, email, username, password):
        user_manager = UserManager(CONNEXION)
        user_registration = user_manager.register_user(first_name, last_name, username, email, password)
        if user_registration:
            CTkMessagebox(title="Info", message="Felicitation votre compte a ete crees")
            registration_app.destroy()
        else:
            CTkMessagebox(title="Error", message="L'utilisateur existe déjà ou l'inscription a échoué!!!", icon="cancel")

def open_registration_page():
    global registration_app, first_name_entry, last_name_entry, email_entry, registration_user_entry, registration_pass_entry
    
    registration_app = ctk.CTk()
    registration_app.geometry("600x560")
    registration_app.title("Page d'Inscription - BUDGET-TRACKER")
    #registration_app.iconbitmap("logo/badgettraker.ico")
    
    label = ctk.CTkLabel(registration_app,font=("", 20,'bold'), text="---BUDGET-TRACKER---")
    label.pack(pady=10)
    
    frame = ctk.CTkFrame(master=registration_app)
    frame.pack(pady=30, padx=40, fill='both', expand=True)
    
    label = ctk.CTkLabel(master=frame, text='Inscription :')
    label.pack(pady=12, padx=50)
    
    first_name_entry = ctk.CTkEntry(master=frame, placeholder_text="Prénom")
    first_name_entry.pack(pady=12, padx=10)
    
    last_name_entry = ctk.CTkEntry(master=frame, placeholder_text="Nom de famille")
    last_name_entry.pack(pady=12, padx=10)
    
    email_entry = ctk.CTkEntry(master=frame, placeholder_text="Email")
    email_entry.pack(pady=12, padx=10)
    
    registration_user_entry = ctk.CTkEntry(master=frame, placeholder_text="Nom d'utilisateur")
    registration_user_entry.pack(pady=12, padx=10)
    
    registration_pass_entry = ctk.CTkEntry(master=frame, placeholder_text="Mot de passe", show="*")
    registration_pass_entry.pack(pady=12, padx=10)
    
    register_button = ctk.CTkButton(master=frame, text="S'inscrire", command=register)
    register_button.pack(pady=12, padx=10)
    
    cancel_button = ctk.CTkButton(master=frame, text='Annuler', command=registration_app.destroy)
    cancel_button.pack(pady=12, padx=10)
    
    Budjet_traker = ctk.CTkLabel(registration_app,font=("", 10), text="© Budjet-traker 2024-2025 Conception et realisation par Med-Mehdi ZMANTAR & Jassem BOUGHATAS. Tous droits reserves.")
    Budjet_traker.pack(pady=10)
    
    registration_app.mainloop()

def Recovery_password():
    global rp_user_entry , rp_email_entry
    username = rp_user_entry.get()
    email = rp_email_entry.get()
    
    user_manager = UserManager(CONNEXION)
    forgot_password = user_manager.get_password(username,email)
    
    if forgot_password:
        CTkMessagebox(title="Info", message="verifier votre mail")
    else:
        CTkMessagebox(title="Error", message="votre username ou votre email invalide!!!", icon="cancel")

def forgot_password():
    global rp_user_entry , rp_email_entry
    password_app = ctk.CTk()
    password_app.geometry("600x470")
    password_app.title("PAGE RECOVER PASSWORD - BUDGET-TRACKER")
    #password_app.iconbitmap("logo/badgettraker.ico")
    label = ctk.CTkLabel(master=password_app,font=("", 20,'bold'),text='---BUDGET-TRACKER---')
    label.pack(pady=12, padx=50, fill='both')
        
    frame = ctk.CTkFrame(master=password_app)
    frame.pack(pady=30, padx=40, fill='both', expand=True)
    
    label_P = ctk.CTkLabel(master=frame, text='Recover Password')
    label_P.pack(pady=12, padx=10, fill='both')
    
    rp_user_entry = ctk.CTkEntry(master=frame, placeholder_text="Username")
    rp_user_entry.pack(pady=12, padx=10)
    
    label_P = ctk.CTkLabel(master=frame, text='--OR:')
    label_P.pack(pady=1, padx=1)
    
    rp_email_entry = ctk.CTkEntry(master=frame, placeholder_text="Email")
    rp_email_entry.pack(pady=12, padx=10)
    
    rp_button_entry = ctk.CTkButton(master=frame, text='Envoyer', command=lambda: Recovery_password())
    rp_button_entry.pack(pady=12, padx=10)
    
    cancel_button = ctk.CTkButton(master=frame, text='Annuler', command=password_app.destroy)
    cancel_button.pack(pady=12)
    
    Budjet_traker = ctk.CTkLabel(password_app,font=("", 10), text="© Budjet-traker 2024-2025 Conception et realisation par Med-Mehdi ZMANTAR & Jassem BOUGHATAS. Tous droits reserves.")
    Budjet_traker.pack(pady=10)
    
    password_app.mainloop()

def login_Page():
    global app
    app = ctk.CTk()
    app.geometry("800x600")
    app.title("PAGE DE CONNEXION - BUDGET-TRACKER")
    #app.iconbitmap("logo/badgettraker.ico")

    # darkmode variable
    global dark_mode_variable
    dark_mode_variable = ctk.IntVar()

    global login_frame
    login_frame = ctk.CTkFrame(master=app, fg_color="transparent")
    login_frame.pack(pady=15, padx=35, fill='both', expand=True)

    label = ctk.CTkLabel(login_frame,font=("ariel", 20,'bold'), text="BUDGET TRACKER")
    label.pack(pady=35, padx=20)

    frame = ctk.CTkFrame(master=login_frame)
    frame.pack(pady=15, padx=35, fill='both', expand=True)

    label = ctk.CTkLabel(master=frame, text='CONNEXION')
    label.pack(pady=7, padx=50)

    username_entry = ctk.CTkEntry(master=frame, placeholder_text="Nom d'utilisateur")
    username_entry.pack(pady=12, padx=10)

    global password_entry
    password_entry = ctk.CTkEntry(master=frame, placeholder_text="Mot de passe", show="*")
    password_entry.pack(pady=12, padx=10)

    button = ctk.CTkButton(master=frame, text='Connexion', command=lambda: login(username_entry, password_entry))
    button.pack(pady=12, padx=10)

    checkbox = ctk.CTkCheckBox(master=frame, text='Se souvenir de moi')
    checkbox.pack(pady=12, padx=10)

    register_link = ctk.CTkLabel(login_frame, text="Pas encore inscrit ? Cliquez ici pour vous inscrire.", cursor="hand2")
    register_link.pack(pady=10)
    register_link.bind("<Button-1>", lambda e: open_registration_page())

    forgot_password_label = ctk.CTkLabel(login_frame, text="Mot de passe oublié ?", cursor="hand2")
    forgot_password_label.pack(pady=10)
    forgot_password_label.bind("<Button-1>", lambda e: forgot_password())

    dark_mode_button = ctk.CTkSwitch(login_frame, onvalue=1, offvalue=0, text='Activer le mode sombre ou clair', variable=dark_mode_variable, command=toggle_dark_mode)
    dark_mode_button.pack(pady=10)

    Budjet_traker = ctk.CTkLabel(login_frame,font=("", 10), text="© Budjet-traker 2024-2025 Conception et realisation par Med-Mehdi ZMANTAR & Jassem BOUGHATAS. Tous droits reserves.")
    Budjet_traker.pack(pady=10)

    app.mainloop()
