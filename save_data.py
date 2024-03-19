from datetime import datetime, timedelta
from time import strftime
from customtkinter import *
from tkcalendar import DateEntry
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from config import *

table = None
get_fetched_id = None
get_fetched_name = None
database_manager = DatabaseManager()

query_all = "SELECT * FROM insertdata"

def add_data(group, start, end, strhour, strmin, ehour, emin, month, type, reason, comment ):
    if not group.get() or not month.get() or not type.get() or not start.get() or not end.get() or not strhour.get() or not strmin.get() or not ehour.get() or not emin.get() or not reason.get("0.0", "end"):
        messagebox.showerror(title="Error", message="Fields marked with an asterisk are required")
        return
    
    #--------------------------------------------------------------------------
    
    #Konvertálom dátum és idő objektummá, algoritmus a számlált napokra
    
    start_date_to_postgresql = datetime.strptime(start.get(), "%m/%d/%y")    #%m/%d/%y
    
    end_date_to_postgresql = datetime.strptime(end.get(), "%m/%d/%y")        #"%Y. %m. %d."

    
    day_diff = end_date_to_postgresql - start_date_to_postgresql

    hours_diff = int(ehour.get()) - int(strhour.get())
    
    min_diff = int(emin.get()) - int(strmin.get())

    #--------------------------------------------------------------------------

    # Kezelem azokat az eseteket, amikor a befejezési időpont korábbi, mint a kezdési időpont
    
    if min_diff < 0:
        hours_diff -= 1
        min_diff += 60

    if hours_diff < 0:
        day_diff -= timedelta(days=1)
        hours_diff += 24

    #--------------------------------------------------------------------------
    
    # máshogy printelem a napokat
        
    diff = f"{day_diff.days} day(s) {hours_diff} hour {min_diff} minutes"

    
    database_manager.curs.execute("INSERT INTO insertdata (user_company_id, name, team_group, month, type, start_date, end_date, start_hour, start_min, end_hour, end_min, reason, comment, counted_day, counted_hour, counted_min, counted_time, approval) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                 (get_fetched_id, get_fetched_name, group.get(), month.get(), type.get(), start_date_to_postgresql.strftime("%Y-%m-%d"), end_date_to_postgresql.strftime("%Y-%m-%d"), strhour.get(), strmin.get(), ehour.get(), emin.get(), reason.get("0.0", "end"), comment.get("0.0", "end"), int(day_diff.days), hours_diff, min_diff, diff, "false"))
    database_manager.conn.commit()

    # delete_data(start, end, strhour, strmin, ehour, emin, reason, comment)
    
    get_data(table)

def get_data(table):
    global get_fetched_id, Class, overtime
    
    # Query csak egy főre

    query_one_user = "SELECT insertdata.* FROM insertdata JOIN registration ON insertdata.user_company_id = registration.user_company_id WHERE registration.user_company_id = :user_id"
    params_one_user = {"user_id": get_fetched_id}
    
    # Query auth level A-val az összes főre
    
    database_manager.curs.execute(query_all if Class == 'A' else query_one_user, params_one_user)
    datas = database_manager.curs.fetchall()
    table.delete(*table.get_children())

    #insert_data(datas)
    #chart_frame(add_data_win, get_fetched_id)
    #user_card()

def insert_data(datas):
    for i, data in enumerate(datas):
        clean_data = ["" if d is None else d for d in data]
        my_tag = 'green' if data[19] == "true" else 'red'
        table.insert("", "end",values=(
            clean_data[20], clean_data[2], clean_data[3], clean_data[6], clean_data[7],
            clean_data[4], clean_data[5], clean_data[12], clean_data[13],
            clean_data[14], clean_data[18], clean_data[19]
        ), tags=('unchecked', my_tag))


def logout(win):
     database_manager.curs.execute("UPDATE registration SET permission = false WHERE user_company_id = ?", (get_fetched_id,))
     database_manager.conn.commit()
     win.destroy()

#save_data()