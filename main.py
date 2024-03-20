from config import DatabaseManager
from login import *

db_manager = DatabaseManager()

db_manager.connect()
login_ui()
db_manager.close()