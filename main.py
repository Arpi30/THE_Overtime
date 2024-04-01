from config import DatabaseManager
from login import *

db_manager = DatabaseManager()

#Adatbázis megnyitása és zárása, bejelentkezés
db_manager.connect()
login_ui()
db_manager.close()