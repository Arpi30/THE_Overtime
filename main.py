from config import DatabaseManager
from login import *

db_manager = DatabaseManager()

db_manager.connect()
print(db_manager.connecting)
login_ui()
db_manager.close()