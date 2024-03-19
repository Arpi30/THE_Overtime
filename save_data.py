from datetime import datetime, timedelta
from time import strftime
from customtkinter import *
from tkcalendar import DateEntry
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from config import *

get_fetched_id = None
get_fetched_name = None
database_manager = DatabaseManager()

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
    
    #máshogy printelem a napokat
        
    diff = f"{day_diff.days} day(s) {hours_diff} hour {min_diff} minutes"

    
    database_manager.curs.execute("INSERT INTO insertdata (user_company_id, name, team_group, month, type, start_date, end_date, start_hour, start_min, end_hour, end_min, reason, comment, counted_day, counted_hour, counted_min, counted_time, approval) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                 (get_fetched_id, get_fetched_name, group.get(), month.get(), type.get(), start_date_to_postgresql.strftime("%Y-%m-%d"), end_date_to_postgresql.strftime("%Y-%m-%d"), strhour.get(), strmin.get(), ehour.get(), emin.get(), reason.get("0.0", "end"), comment.get("0.0", "end"), int(day_diff.days), hours_diff, min_diff, diff, "false"))
    database_manager.conn.commit()

    delete_data(start, end, strhour, strmin, ehour, emin, reason, comment)
    get_data(table)