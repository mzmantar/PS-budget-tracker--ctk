import re
import customtkinter as ctk
import customtkinter

from main import UserManager
from CTkMessagebox import CTkMessagebox
from Connexion import CONNEXION

customtkinter.set_appearance_mode("light")

def toggle_dark_mode():
    global dark_mode_button
    if dark_mode_button.get():
        ctk.set_appearance_mode("dark")
    else:
        ctk.set_appearance_mode("light")

def destroy_window():
    global dashbord_BT
    dashbord_BT.destroy()
    login_Page()
    
def perform_update(old_username, new_firstname_entry, new_lastname_entry, new_email_entry, old_password_entry, new_password_entry):
    global register_button
    username = old_username.get()
    new_firstname = new_firstname_entry.get()
    new_lastname = new_lastname_entry.get()
    new_email = new_email_entry.get()
    old_password = old_password_entry.get()
    new_password = new_password_entry.get()
    
    user_manager = UserManager(CONNEXION)
    update_success = user_manager.update_user(username,old_password, new_firstname, new_lastname, new_email, new_password)
        
    if update_success:
        CTkMessagebox(title="Info", message="Félicitations, votre profil a été mis à jour avec succès.")
        register_button.destroy()
        login_Page()
        
    else:
        CTkMessagebox(title="Erreur", message="Échec de la mise à jour du profil. Veuillez vérifier vos informations.", icon="cancel")

def update_user():
    global register_button
    update_user_window = ctk.CTk()
    update_user_window.geometry("800x700")
    update_user_window.title("MISE À JOUR DU PROFIL - BUDGET-TRACKER")
    
    label = ctk.CTkLabel(update_user_window, font=("", 20, 'bold'), text="---BUDGET-TRACKER---")
    label.pack(pady=10)
    
    frame = ctk.CTkFrame(master=update_user_window)
    frame.pack(pady=30, padx=40, fill='both', expand=True)
    
    label = ctk.CTkLabel(master=frame, text='Mise à jour du profil :')
    label.pack(pady=12, padx=50)
    
    label = ctk.CTkLabel(master=frame, font=("", 15, 'bold'), text='Attention !!!Le nom utilisateur ne peut pas être modifié.!!!')
    label.pack(pady=12, padx=50)
    
    old_username_entry = ctk.CTkEntry(master=frame, placeholder_text="Nom d'utilisateur")
    old_username_entry.pack(pady=12, padx=10)
    
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
                                     command=lambda: perform_update(old_username_entry, new_firstname_entry, new_lastname_entry, new_email_entry, old_password_entry, new_password_entry))
    register_button.pack(pady=12, padx=10)
    
    cancel_button = ctk.CTkButton(master=frame, text='Annuler', command=update_user_window.destroy)
    cancel_button.pack(pady=12, padx=10)
    
    budget_tracker_label = ctk.CTkLabel(update_user_window, font=("", 10), text="© Budget-tracker 2024-2025 Conception et réalisation par Med-Mehdi ZMANTAR & Jassem BOUGHATAS. Tous droits réservés.")
    budget_tracker_label.pack(pady=10)
    
    update_user_window.mainloop()

  

def login():
    username = username_entry.get()
    password = password_entry.get()
    
    user_manager = UserManager(CONNEXION)
    User = user_manager.login_user(username, password)
    
    if User:
        msg = CTkMessagebox(title="Exit?", message="Connexion réussie.",
                        icon="question", option_1="Cancel",option_3="Yes")
        response = msg.get()
        if response=="Yes":
            app.destroy()
            global dashbord_BT,dark_mode_button,user_id
            row = user_manager.get_firstname_lastname(username)
            dashbord_BT = ctk.CTk()
            dashbord_BT.geometry("1200x700")
            dashbord_BT.title("PAGE RECOVER PASSWORD - BUDGET-TRACKER")
            dashbord_BT.iconbitmap("logo/badgettraker.ico")
            
            
            Dec_button = ctk.CTkButton(master=dashbord_BT, text='DECONNEXION', command=destroy_window)
            Dec_button.pack(side='top', anchor='ne', padx=20, pady=20)
            
            user_id = ctk.CTkLabel(dashbord_BT, font=("",15), text=f"Bonjour {row.upper()}", cursor="hand2")
            user_id.pack(side='top', anchor='w', padx=35, pady=20)
            user_id.bind("<Button-1>", lambda event: update_user())
            

            label = ctk.CTkLabel(master=dashbord_BT, font=("", 20, 'bold'), text='---BUDGET-TRACKER---')
            label.pack(pady=2, padx=10, fill='both')

            frame2 = ctk.CTkFrame(master=dashbord_BT)
            frame2.pack(side='right', pady=200, padx=15, fill='both')


            frame1 = ctk.CTkFrame(master=dashbord_BT)
            frame1.pack(side='left', pady=200, padx=15, fill='both')

            frame = ctk.CTkFrame(master=dashbord_BT)
            frame.pack(pady=100, padx=5, fill='both', expand=True)
            
            dark_mode_button = ctk.CTkSwitch(dashbord_BT, onvalue=1, offvalue=0, text='Activer le mode sombre ou clair', command=toggle_dark_mode)
            dark_mode_button.pack(pady=10)

            Budjet_traker = ctk.CTkLabel(dashbord_BT, font=("", 10), text="© Budget-tracker 2024-2025 Conception et réalisation par Med-Mehdi ZMANTAR & Jassem BOUGHATAS. Tous droits réservés.")
            Budjet_traker.pack(pady=10)

            dashbord_BT.mainloop()
        else:
            app.destroy()
            login_Page()
                        
    else:
        CTkMessagebox(title="Error", message="Nom d'utilisateur ou mot de passe invalide.!!!", icon="cancel")


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
    registration_app.iconbitmap("logo/badgettraker.ico")
    
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
    password_app.iconbitmap("logo/badgettraker.ico")
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
    global app, dark_mode_button
    app = ctk.CTk()
    app.geometry("800x600")
    app.title("PAGE DE CONNEXION - BUDGET-TRACKER")
    app.iconbitmap("logo/badgettraker.ico")

    label = ctk.CTkLabel(app,font=("", 20,'bold'), text="---BUDGET-TRACKER---")
    label.pack(pady=10)

    frame = ctk.CTkFrame(master=app)
    frame.pack(pady=50, padx=30, fill='both', expand=True)

    label = ctk.CTkLabel(master=frame, text='CONNEXION')
    label.pack(pady=7, padx=50)
    global username_entry
    username_entry = ctk.CTkEntry(master=frame, placeholder_text="Nom d'utilisateur")
    username_entry.pack(pady=12, padx=10)
    global password_entry
    password_entry = ctk.CTkEntry(master=frame, placeholder_text="Mot de passe", show="*")
    password_entry.pack(pady=12, padx=10)

    button = ctk.CTkButton(master=frame, text='Connexion', command=lambda: login())
    button.pack(pady=12, padx=10)

    checkbox = ctk.CTkCheckBox(master=frame, text='Se souvenir de moi')
    checkbox.pack(pady=12, padx=10)

    register_link = ctk.CTkLabel(app, text="Pas encore inscrit ? Cliquez ici pour vous inscrire.", cursor="hand2")
    register_link.pack(pady=10)
    register_link.bind("<Button-1>", lambda e: open_registration_page())

    forgot_password_label = ctk.CTkLabel(app, text="Mot de passe oublié ?", cursor="hand2")
    forgot_password_label.pack(pady=10)
    forgot_password_label.bind("<Button-1>", lambda e: forgot_password())

    dark_mode_button = ctk.CTkSwitch(app,onvalue=1,offvalue=0, text='Activer le mode dark ou light' ,command=toggle_dark_mode)
    dark_mode_button.pack(pady=10)

    Budjet_traker = ctk.CTkLabel(app,font=("", 10), text="© Budjet-traker 2024-2025 Conception et realisation par Med-Mehdi ZMANTAR & Jassem BOUGHATAS. Tous droits reserves.")
    Budjet_traker.pack(pady=10)

    app.mainloop()
