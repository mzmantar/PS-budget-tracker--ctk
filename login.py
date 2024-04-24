import customtkinter as ctk

def login():
    print("Username:", user_entry.get())
    print("Password:", user_pass.get())

def validate_email(email):
    # Validation de l'email par une expression régulière
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        print("Invalid email address.")
        return False
    return True

def validate_registration(first_name, last_name, email, username, password):
    # Validation des champs du formulaire d'inscription
    if not all([first_name, last_name, email, username, password]):
        print("Please fill in all fields.")
        return False
    if not validate_email(email):
        return False
    return True

def register():
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    email = email_entry.get()
    username = registration_user_entry.get()
    password = registration_pass_entry.get()

    if validate_registration(first_name, last_name, email, username, password):
        print("First Name:", first_name)
        print("Last Name:", last_name)
        print("Email:", email)
        print("Username:", username)
        print("Password:", password)

def open_registration_page():
    registration_window = ctk.CTk()
    registration_window.geometry("500x400")
    registration_window.title("Inscription")

    label = ctk.CTkLabel(registration_window, text="Inscription", font=("Helvetica", 24))
    label.pack(pady=20)

    frame = ctk.CTkFrame(master=registration_window)
    frame.pack(pady=20, padx=40, fill='both', expand=True)

    # First Name
    first_name_label = ctk.CTkLabel(master=frame, text='Prénom:')
    first_name_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')

    global first_name_entry
    first_name_entry = ctk.CTkEntry(master=frame, placeholder_text="First Name")
    first_name_entry.grid(row=0, column=1, padx=10, pady=10)

    # Last Name
    last_name_label = ctk.CTkLabel(master=frame, text='Nom de famille:')
    last_name_label.grid(row=1, column=0, padx=10, pady=10, sticky='w')

    global last_name_entry
    last_name_entry = ctk.CTkEntry(master=frame, placeholder_text="Last Name")
    last_name_entry.grid(row=1, column=1, padx=10, pady=10)

    # Email
    email_label = ctk.CTkLabel(master=frame, text='Email:')
    email_label.grid(row=2, column=0, padx=10, pady=10, sticky='w')

    global email_entry
    email_entry = ctk.CTkEntry(master=frame, placeholder_text="Email")
    email_entry.grid(row=2, column=1, padx=10, pady=10)

    # Username
    username_label = ctk.CTkLabel(master=frame, text='Nom d\'utilisateur:')
    username_label.grid(row=3, column=0, padx=10, pady=10, sticky='w')

    global registration_user_entry
    registration_user_entry = ctk.CTkEntry(master=frame, placeholder_text="Username")
    registration_user_entry.grid(row=3, column=1, padx=10, pady=10)

    # Password
    password_label = ctk.CTkLabel(master=frame, text='Mot de passe:')
    password_label.grid(row=4, column=0, padx=10, pady=10, sticky='w')

    global registration_pass_entry
    registration_pass_entry = ctk.CTkEntry(master=frame, placeholder_text="Password", show="*")
    registration_pass_entry.grid(row=4, column=1, padx=10, pady=10)

    register_button = ctk.CTkButton(master=frame, text='Register', command=register)
    register_button.grid(row=5, column=1, padx=15, pady=10)

    registration_window.mainloop()

def forgot_password():
    print("Forgot Password")

app = ctk.CTk()
app.geometry("800x500")
app.title("LOGIN PAGE--BUDGET-TRACKER")

label = ctk.CTkLabel(app, text="---BUDGET-TRACKER---")
label.pack(pady=10)

frame = ctk.CTkFrame(master=app)
frame.pack(pady=20, padx=40, fill='both', expand=True)

label = ctk.CTkLabel(master=frame, text='CONNEXION :')
label.pack(pady=12, padx=10)

user_entry = ctk.CTkEntry(master=frame, placeholder_text="Username")
user_entry.pack(pady=12, padx=10)

user_pass = ctk.CTkEntry(master=frame, placeholder_text="Password", show="*")
user_pass.pack(pady=12, padx=10)

button = ctk.CTkButton(master=frame, text='Login', command=login)
button.pack(pady=12, padx=10)

checkbox = ctk.CTkCheckBox(master=frame, text='Remember Me')
checkbox.pack(pady=12, padx=10)

register_link = ctk.CTkLabel(app, text="Pas encore inscrit ? Cliquez ici pour vous inscrire.", cursor="hand2")
register_link.pack(pady=10)
register_link.bind("<Button-1>", lambda e: open_registration_page())

forgot_password_label = ctk.CTkLabel(app, text="Mot de passe oublié ?", cursor="hand2")
forgot_password_label.pack(pady=10)
forgot_password_label.bind("<Button-1>", lambda e: forgot_password())

app.mainloop()
