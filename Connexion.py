import mysql.connector 
from main import *
CONNEXION = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="",
    database="projet_s"
)

if CONNEXION:
    print("CONNEXION établie avec succès")
else:
    print("ERREUR DE CONNEXION")

