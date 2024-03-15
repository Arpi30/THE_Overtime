from customtkinter import *
from config import *
from PIL import ImageTk, Image
from tkcalendar import DateEntry
import tkinter as tk
from tkinter import ttk


add_data_win = None
table = None
add_data_frame = None
get_fetched_id = None
get_fetched_name = None
Class = None
database_manager = DatabaseManager()
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
  #Menu
  mainmenu  = tk.Menu(add_data_win)
  file_menu = tk.Menu(mainmenu, tearoff=0)
  file_menu.add_command(label="Exit",font="Helvetica 8 bold")
  
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
  
  delete_all_button = CTkButton(add_data_frame, text="Delete all")
  add_button = CTkButton(add_data_frame, text="Add")
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
  cols = ("ID", "Name", "Group", "Start", "End", "Month", "Type", "Reason", "Comment", "Negative time", "Counted Time", "Approval")
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
  add_data_win.mainloop()