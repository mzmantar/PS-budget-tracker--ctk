import re
import customtkinter as ctk
import customtkinter
from main import UserManager

def login():
    username = username_entry.get()
    password = password_entry.get()
    
    user_manager = UserManager()
    user = user_manager.login_user(username, password)
    
    if user:
        print("Connexion réussie.")
        import dashboard
        button.destroy()
        dashboard.show_login()
    else:
        print("Nom d'utilisateur ou mot de passe invalide.")

def validate_email(email):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        print("Adresse email invalide.")
        return False
    return True

def validate_registration(first_name, last_name, email, username, password):
    if not all([first_name, last_name, email, username, password]):
        print("Remplissez tous les champs.")
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
        user_manager = UserManager()
        user_registration = user_manager.register_user(first_name, last_name, username, email, password)
        if user_registration:
            print("Inscription réussie.")
        else:
            print("L'utilisateur existe déjà ou l'inscription a échoué.")

def open_registration_page():
    global first_name_entry, last_name_entry, email_entry, registration_user_entry, registration_pass_entry
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

def forgot_password():
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
    
    rp_button_entry = ctk.CTkButton(master=frame, text='Envoyer')
    rp_button_entry.pack(pady=12, padx=10)
    
    cancel_button = ctk.CTkButton(master=frame, text='Annuler', command=password_app.destroy)
    cancel_button.pack(pady=12)
    
    Budjet_traker = ctk.CTkLabel(password_app,font=("", 10), text="© Budjet-traker 2024-2025 Conception et realisation par Med-Mehdi ZMANTAR & Jassem BOUGHATAS. Tous droits reserves.")
    Budjet_traker.pack(pady=10)
    
    password_app.mainloop()


customtkinter.set_appearance_mode("light")

def toggle_dark_mode():
    if dark_mode_button.get():
        ctk.set_appearance_mode("dark")
    else:
        ctk.set_appearance_mode("light")
        
    
    
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

username_entry = ctk.CTkEntry(master=frame, placeholder_text="Nom d'utilisateur")
username_entry.pack(pady=12, padx=10)

password_entry = ctk.CTkEntry(master=frame, placeholder_text="Mot de passe", show="*")
password_entry.pack(pady=12, padx=10)

button = ctk.CTkButton(master=frame, text='Connexion', command=login)
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
print(dark_mode_button.get())

Budjet_traker = ctk.CTkLabel(app,font=("", 10), text="© Budjet-traker 2024-2025 Conception et realisation par Med-Mehdi ZMANTAR & Jassem BOUGHATAS. Tous droits reserves.")
Budjet_traker.pack(pady=10)


app.mainloop()
