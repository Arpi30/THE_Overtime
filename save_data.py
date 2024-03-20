from customtkinter import *
from config import *
from PIL import ImageTk, Image
from tkcalendar import DateEntry
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime, timedelta
from time import strftime

database_manager = DatabaseManager()
#Globális változók
add_data_win = None
table = None
add_data_frame = None
get_fetched_id = None
get_fetched_name = None
Class = None
my_tag = 'normal'

today_date = None
overtime = 0
standby = 0
sliding = 0
clock = None
query_all = "SELECT * FROM insertdata"


def save_data():
  global table, add_data_win, get_fetched_id, get_fetched_name, Class, today_date, overtime, standby, sliding, clock
  add_data_win = CTk()
  add_data_win.title("Login employee manager")
  add_data_win.geometry('1400x850')
  set_appearance_mode("light")
  add_data_win.resizable(False, False)
  user_card()
  #Menu
  mainmenu  = tk.Menu(add_data_win)
  file_menu = tk.Menu(mainmenu, tearoff=0)
  file_menu.add_command(label="Exit",font="Helvetica 8 bold", command=lambda: logout(add_data_win))
  
  mainmenu.add_cascade(label="Menu", menu=file_menu, font="Helvetica 10")
  add_data_win.config(menu=mainmenu)
  #Add Data Frame into window
  add_data_frame = CTkFrame(add_data_win, width=800, height=300, border_width=3, fg_color=("#edebeb"))
  add_data_frame.place(x=5, y=5)
  #Add data Frame label

  clock = CTkLabel(add_data_frame, font=("Calibri", 40))
  group_label= CTkLabel(add_data_frame, text="* Group", font=("Arial", 16))
  month_label= CTkLabel(add_data_frame, text="* Month", font=("Arial", 16))
  type_label= CTkLabel(add_data_frame, text="* Type", font=("Arial", 16))
  start_date_label= CTkLabel(add_data_frame, text="* Start date", font=("Arial", 16))
  end_date_label= CTkLabel(add_data_frame, text="* End date", font=("Arial", 16))
  reason_label= CTkLabel(add_data_frame, text="* Reason", font=("Arial", 16))
  comment_label= CTkLabel(add_data_frame, text="Comment", font=("Arial", 16))
  #Add data Frame Entry
  start_hour_str = tk.StringVar()
  start_min_str = tk.StringVar()
  end_hour_str = tk.StringVar()
  end_min_str = tk.StringVar()
  start_hour = ttk.Spinbox(add_data_frame, from_=0, to=23, textvariable=start_hour_str, width=3, value=0)
  start_min = ttk.Spinbox(add_data_frame, from_=0, to=60, textvariable=start_min_str, width=3, value=0)
  end_hour = ttk.Spinbox(add_data_frame, from_=0, to=23, textvariable=end_hour_str, width=3, value=0)
  end_min = ttk.Spinbox(add_data_frame, from_=0, to=60, textvariable=end_min_str, width=3, value=0)
  group_omenu= CTkOptionMenu(add_data_frame, values=["App1", "App2"])
  month_omenu= CTkOptionMenu(add_data_frame, values=["Január", "Február", "Március", "Április", "Május", "Június", "Július", "Augusztus", "Szeptember", "Október", "November", "December"])
  type_omenu= CTkOptionMenu(add_data_frame, values=["Túlóra", "Készenlét", "Csúszó"])
  calendar_start_entry = DateEntry(add_data_frame, selectmode = 'day', year = 2024, month = 1, day = 1, background='darkblue', foreground='white', borderwidth=2)
  calendar_end_entry = DateEntry(add_data_frame, selectmode = 'day', year = 2024, month = 1, day = 1, background='darkblue', foreground='white', borderwidth=2)
  reason_textBox = CTkTextbox(add_data_frame, width=250, height=30, border_width=1)
  comment_textBox = CTkTextbox(add_data_frame, width=250, height=30, border_width=1)
  #Button
  
  delete_all_button = CTkButton(add_data_frame, text="Delete all", command=lambda: delete_data( 
                                                                              calendar_start_entry, calendar_end_entry,start_hour, start_min, end_hour, end_min, 
                                                                              reason_textBox,comment_textBox))
  add_button = CTkButton(add_data_frame, text="Add", command=lambda: add_data(group_omenu, 
                                                                              calendar_start_entry, calendar_end_entry,start_hour, start_min, end_hour, end_min, 
                                                                              month_omenu, type_omenu, reason_textBox,comment_textBox))
  if Class == "A":
    file_menu.add_separator()
    file_menu.add_command(label="Edit profile",font="Helvetica 8 bold")
    export_to_excel = CTkButton(add_data_frame,text="Export to excel")
    export_to_excel.place(x=460, y=260)
    search_entry = CTkEntry(add_data_win, font=("Arial", 14), placeholder_text="Search")
    search_entry.place(x=15, y=325)
    search_button = CTkButton(add_data_win,text="Search")
    search_button.place(x=175, y=325)
    toplevel_button_ok = CTkButton(add_data_win, text="OK", width=50)
    toplevel_button_ok.bind('<Button 1>')
    toplevel_button_can = CTkButton(add_data_win, text="NOK", width=50)
    toplevel_button_can.bind('<Button 1>')
    toplevel_button_ok.place(x=1300, y=325)
    toplevel_button_can.place(x=1300, y=365)
    delete_rows = CTkButton(add_data_win, text="Delete")
    delete_rows.place(x=15, y=365)


  #Place label and Entry on the Frame

  clock.place(x=460, y=200)
  group_label.place(x=10, y=10)
  month_label.place(x=10, y=40)
  type_label.place(x=10, y=70)
  start_date_label.place(x=10, y=100)
  end_date_label.place(x=10, y=130)
  reason_label.place(x=10, y=160)
  comment_label.place(x=15, y=195)
  #Entry
  group_omenu.place(x=100, y=10)
  month_omenu.place(x=100, y=40)
  type_omenu.place(x=100, y=70)
  calendar_start_entry.place(x=100, y=105)
  calendar_end_entry.place(x=100, y=135)

  start_hour.place(x=200, y=105)
  start_min.place(x=240, y=105)
  end_hour.place(x=200, y=135)
  end_min.place(x=240, y=135)
  reason_textBox.place(x=100, y=165)
  comment_textBox.place(x=100, y=200)
  add_button.place(x=10, y=260)
  delete_all_button.place(x=170, y=260)

  #Add Table Frame to window
  table_frame = CTkFrame(add_data_win)
  table_frame.place(x=5, y=400)
  #add coll title
  cols = ("Name", "Group", "Start", "End", "Month", "Type", "Reason", "Comment", "Negative time", "Counted Time", "Approval")
  table = ttk.Treeview(table_frame, columns=cols, height=20)
  scrollbar = CTkScrollbar(table_frame, command=table.yview)
  
  table.tag_configure('green', background='#d1facf')
  table.tag_configure('red', background='#ffffff')
  for col in cols:
        table.heading(col, text=col, anchor='center')
        table.column(col, width=112, anchor="center")
        table.column("#0", width=28, anchor="ne")
  table.pack(side="left", fill="y")
  table.configure(yscrollcommand=scrollbar.set)
  scrollbar.pack(side="right", fill="y")
  delete_data(calendar_start_entry, calendar_end_entry,start_hour, start_min, end_hour, end_min,reason_textBox,comment_textBox)
  get_data(table)
  time()
  add_data_win.mainloop()

def add_data(group, start, end, strhour, strmin, ehour, emin, month, type, reason, comment ):
    if not group.get() or not month.get() or not type.get() or not start.get() or not end.get() or not strhour.get() or not strmin.get() or not ehour.get() or not emin.get() or not reason.get("0.0", "end"):
        messagebox.showerror(title="Error", message="Fields marked with an asterisk are required")
        return
    
    #--------------------------------------------------------------------------
    
    #Konvertálom dátum és idő objektummá, algoritmus a számlált napokra
    start_date_to_postgresql = datetime.strptime(start.get(), "%Y. %m. %d.")    #%m/%d/%y       -> legenerált exe-vel
    end_date_to_postgresql = datetime.strptime(end.get(), "%Y. %m. %d.")        #"%Y. %m. %d."  -> vscode-ban
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

    delete_data(start, end, strhour, strmin, ehour, emin, reason, comment)
    get_data(table)

#--------------------------------------------------------------------------

def get_data(table):
    global get_fetched_id, Class, overtime

    #--------------------------------------------------------------------------   
   
    # Query csak egy főre
    query_one_user = "SELECT insertdata.* FROM insertdata JOIN registration ON insertdata.user_company_id = registration.user_company_id WHERE registration.user_company_id = :user_id"
    params_one_user = {"user_id": get_fetched_id}
    
    #--------------------------------------------------------------------------
   
    # Query auth level A-val az összes főre
    database_manager.curs.execute(query_all if Class == 'A' else query_one_user, params_one_user)
    datas = database_manager.curs.fetchall()
    table.delete(*table.get_children())

    insert_data(datas)
    #chart_frame(add_data_win, get_fetched_id)
    user_card()

#--------------------------------------------------------------------------

def user_card():
    global get_fetched_id, get_fetched_name, Class, today_date, overtime, standby, sliding
    database_manager.curs.execute('''SELECT registration.user_company_id, 
                                                registration.name, registration.class, 
                                                registration.last_login, 
                                                COALESCE(COUNT(CASE WHEN insertdata.type = 'Túlóra' THEN 1 END),0), 
                                                COALESCE(COUNT(CASE WHEN insertdata.type = 'Készenlét' THEN 1 END),0), 
                                                COALESCE(COUNT(CASE WHEN insertdata.type = 'Csúszó' THEN 1 END),0) 
                                        FROM registration 
                                        LEFT JOIN insertdata ON registration.user_company_id = insertdata.user_company_id 
                                        WHERE registration.permission = true 
                                        GROUP BY registration.user_company_id, registration.name, registration.class''')
    user_data = database_manager.curs.fetchall()

    for data in user_data:
        get_fetched_id = data[0]
        get_fetched_name = data[1]
        Class = data[2]
        today_date = data[3]#.strftime("%Y-%m-%d %H:%M")
        overtime = data[4]
        standby = data[5]
        sliding = data[6]
    #Card Label
    CIAM_label= CTkLabel(add_data_frame, text=f"CIAM ID: {get_fetched_id}", font=("Arial", 16, 'bold'))
    name_label= CTkLabel(add_data_frame, text=f"NAME: {get_fetched_name}", font=("Arial", 16, 'bold'))
    llogin_label= CTkLabel(add_data_frame, text=f"Last login: {today_date}", font=("Arial", 16, 'bold'))
    authL_label= CTkLabel(add_data_frame, text=f"authorization level: {Class}", font=("Arial", 16, 'bold'))
    overtime_label= CTkLabel(add_data_frame, text=f"Overtime: {overtime}", font=("Arial", 16, 'bold'))
    standby_label= CTkLabel(add_data_frame, text=f"Standby: {standby}", font=("Arial", 16, 'bold'))
    sliding_label= CTkLabel(add_data_frame, text=f"Sliding: {sliding}", font=("Arial", 16, 'bold'))
    CIAM_label.place(x=460, y=10)
    name_label.place(x=630, y=10)
    llogin_label.place(x=460, y=40)
    authL_label.place(x=460, y=70)
    overtime_label.place(x=460, y=100)
    standby_label.place(x=460, y=130)
    sliding_label.place(x=460, y=160)

#--------------------------------------------------------------------------
    
def insert_data(datas):
    for i, data in enumerate(datas):
        clean_data = ["" if d is None else d for d in data]
        my_tag = 'green' if data[19] == "true" else 'red'
        table.insert("", "end",values=(
            clean_data[20], clean_data[2], clean_data[3], clean_data[6], clean_data[7],
            clean_data[4], clean_data[5], clean_data[12], clean_data[13],
            clean_data[14], clean_data[18], clean_data[19]
        ), tags=('unchecked', my_tag))

#--------------------------------------------------------------------------
        #Input mező törlés
def delete_data(start, end, strhour, strmin, ehour, emin, reason, comment ):
    start.delete(0, 'end')
    end.delete(0, 'end')
    strhour.delete(0, 'end')
    strmin.delete(0, 'end')
    ehour.delete(0, 'end')
    emin.delete(0, 'end')
    reason.delete("0.0", "end")
    comment.delete("0.0", "end")


#--------------------------------------------------------------------------
def time():
  stringtime = strftime('%H:%M:? %p')
  clock.configure(text=stringtime)
  clock.after(1000,time)


#--------------------------------------------------------------------------
    #Rekord törlés a DB-ből valamint a Treeview-ból is
def del_rows():
    sel_row = CTkLabel(add_data_win, text="")
    sel_row.place(x=630, y=335)
    selected_rows = table.selection()
    if len(selected_rows) == 0:
        sel_row.configure(text="No rows selected", text_color=("#f09999"), font=("Arial", 18))
    else:
        for rowid in selected_rows:
            tags = table.item(rowid, "tags")
            if "checked" in tags and Class == "A":
                get_row = table.item(rowid, "values")[0]
                
                database_manager.curs.execute("DELETE FROM insertdata WHERE row_id = ?", (get_row,))
                database_manager.conn.commit()
            else:
                table.item(rowid, tags=('unchecked', my_tag))
                return
    get_data(table)
    
    
def logout(win):
     database_manager.curs.execute("UPDATE registration SET permission = false WHERE user_company_id = ?", (get_fetched_id,))
     database_manager.conn.commit()
     win.destroy()

save_data()
