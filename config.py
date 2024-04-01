#Adatbázis létrehozása sqlite3-ban
import sqlite3

#DatabaseManager objektum létrehozása
class DatabaseManager:
    def __init__(self):
        #A kapcsolati, kurzor, kapcsolati változók létrehozása
        self.conn = None
        self.curs = None
        self.connecting = ""
        self.connect()

    #A kapcsolat létrehozása
    def connect(self):
        self.connecting = 'Connecting to the SQLite database...'
        #Kapcsolódás az adatbázishoz
        self.conn = sqlite3.connect("the_overtime.db")
        #Kurzor inicializálása
        self.curs = self.conn.cursor()
        #A registration tábla és a benne lévő oszlopok létrehozása
        self.curs.execute("""CREATE TABLE IF NOT EXISTS registration (
                                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                user_company_id VARCHAR(255) NOT NULL,
                                email_address VARCHAR(255) NOT NULL,
                                password VARCHAR(255) NOT NULL,
                                permission BOOLEAN NOT NULL,
                                name VARCHAR(255) NULL,
                                class TEXT NULL,
                                last_login TIMESTAMP,
                                UNIQUE(user_company_id, email_address, name),
                                PRIMARY KEY(user_company_id)
                              )""")
        #Az insertdata tábla és a benne lévő oszlopok létrehozása
        self.curs.execute("""CREATE TABLE IF NOT EXISTS insertdata (
                                user_company_id VARCHAR(255) REFERENCES registration(user_company_id) ON DELETE CASCADE,
                                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                name VARCHAR(255) NOT NULL,
                                team_group VARCHAR(255) NOT NULL,
                                month VARCHAR(255) NOT NULL,
                                type VARCHAR(255) NOT NULL,
                                start_date  DATE NOT NULL,
                                end_date  DATE NOT NULL,
                                start_hour INTEGER NOT NULL,
                                start_min INTEGER NOT NULL,
                                end_hour INTEGER NOT NULL,
                                end_min INTEGER NOT NULL,
                                reason VARCHAR(255) NOT NULL,
                                comment VARCHAR(255) NOT NULL,
                                negative_time INTEGER,
                                counted_day INTEGER NOT NULL,
                                counted_hour INTEGER NOT NULL,
                                counted_min INTEGER NOT NULL,
                                counted_time VARCHAR(255) NOT NULL,
                                approval BOOLEAN,
                                row_id INTEGER,
                                UNIQUE(user_company_id, type, start_date, end_date, start_hour, end_hour),
                                PRIMARY KEY(row_id)  
                              )""")

    #A kapcsolat bontása
    def close(self):
        if self.conn and self.curs:
            self.conn.close()
            self.curs.close()