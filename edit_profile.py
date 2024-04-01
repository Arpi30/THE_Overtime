from tkinter import ttk
from config import DatabaseManager
from customtkinter import *

database_manager = DatabaseManager()
edit_profile_table = None
edit = None

def edit_profile(fetched_id):
    #globális változó
    global edit_profile_table, edit
    #profil szerkesztő ablak inicializálása: focus,cím,méret,mód
    edit = CTkToplevel()
    edit.grab_set()
    edit.title("Edit profile")
    edit.geometry('500x500')
    set_appearance_mode("light")
    edit.resizable(False, False)

    #edit gomb hozzáadása a frame-hez
    edit_profile_table_frame = CTkFrame(edit)
    edit_profile_table_frame.place(x=3, y=50)
    
    #oszlopok hozzáadása a Treeview-hoz
    cols = ("Name", "ID", "Class")
    edit_profile_table = ttk.Treeview(edit_profile_table_frame, columns=cols, height=12)
    scrollbar = CTkScrollbar(edit_profile_table_frame, command=edit_profile_table.yview)

    #oszlopok elhelyezése, berendezése 
    for col in cols:
      edit_profile_table.heading(col, text=col, anchor='center')
      edit_profile_table.column(col, width=154, anchor="center")
      edit_profile_table.column("#0", width=28, anchor="ne")
    edit_profile_table.pack(side="left", fill="y")
    edit_profile_table.configure(yscrollcommand=scrollbar.set)
    #Adatok lekérése db-ből
    get_data()    
    #Felhasználó törlése gomb
    del_member = CTkButton(edit, text="Delete member", command=lambda:delete_member(fetched_id, edit))
    del_member.place(x=190, y=350)
    #Felhasználói adaotk módosítása esemény
    edit.bind("<Double-Button-1>", lambda event: update_profile(event, edit_profile_table))


    edit.mainloop()



def get_data():
   
   #Adatok lekérése db-ből
   database_manager.curs.execute("SELECT name, user_company_id, class FROM registration")
   datas = database_manager.curs.fetchall()
   #Minden lekérésnél törölni kell a Treeview-t
   edit_profile_table.delete(*edit_profile_table.get_children())

   #Lekért adatok végig iterálása és elhelyezése a Treeview-ban
   for i, data in enumerate(datas):
    clean_data = ["" if d is None else d for d in data]
    edit_profile_table.insert("", "end",values=(clean_data[0], clean_data[1], clean_data[2]))


def delete_member(fetched_id, win):
    #Felhasználó kiválasztása
   notapproved_delete_member = CTkLabel(win, text="", font=("Arial", 14, "bold"))
   notapproved_delete_member.pack()
   item = edit_profile_table.selection()
   values = edit_profile_table.item(item, "values")
 
   #Felhasználó törlése a db-ből
   database_manager.curs.execute("DELETE FROM registration WHERE user_company_id = ? AND NOT user_company_id= ?", (values[1], fetched_id,))
   database_manager.conn.commit()
   
   #A felhasználó nem törölheti saját magát
   if fetched_id == values[1]:
      notapproved_delete_member.configure(text="This member cannot be deleted!", text_color=("#f09999"))
   #Adatok lekérése db-ből
   get_data()

def update_profile(event, table):
   #Cella kijelölése
   region_clicked = table.identify_region(event.x, event.y)
   #Hibakezelése ha a cella nem "cell" típusú hanem pl.: header
   if region_clicked not in ("cell"):
      return
   
   #kiválasztott elem
   column = table.identify_column(event.x)
   column_index = int(column[1:]) - 1
   selected_iid = table.focus()
   selected_values = table.item(selected_iid).get("values")[column_index]
   column_box = table.bbox(selected_iid, column)

   #Entry widget elhelyezése a módsoításhoz
   entry_edit = ttk.Entry(table, width=column_box[2])

   #A tartalom elhelyezése az Entry widget-ben
   entry_edit.editing_column_index = column_index
   entry_edit.editing_item_iid = selected_iid
   entry_edit.insert(0, selected_values)
   entry_edit.select_range(0, 'end')
   entry_edit.focus()

   entry_edit.place(x=column_box[0], y=column_box[1], w=column_box[2], h=column_box[3])
   #Focus elvesztése esemény hozzáadása
   entry_edit.bind("<FocusOut>", focus_out)
   entry_edit.bind("<Return>", lambda event: enter_pressed(event, table))

def focus_out(event):
   #Fókusz levélete az adott widget-ről
   event.widget.destroy()

def enter_pressed(event, table):
   global edit
   #Új szöveg
   new_text = event.widget.get()

   #Szelektálás iid és index alapján
   selected_iid = event.widget.editing_item_iid
   column_index = event.widget.editing_column_index

   #Ay aktuális szöveg kiválasztása
   current_values = table.item(selected_iid).get("values")

   #A cella update-elése
   current_values[column_index] = new_text
   table.item(selected_iid, values=current_values)

   update_label = CTkLabel(edit, text="", font=("Arial", 14, "bold"))
   update_label.place(x=80, y=400)

   #DB update-elése
   if column_index == 0:
    database_manager.curs.execute("UPDATE registration SET name = ? WHERE user_company_id = ?", (new_text, current_values[1],))
    database_manager.curs.execute("UPDATE insertdata SET name = ? WHERE user_company_id = ?", (new_text, current_values[1],))
    database_manager.conn.commit()
    update_label.configure(text="To make a full data change, user must log in again!", text_color=("#f09999"))
   elif column_index == 1:
    database_manager.curs.execute("UPDATE registration SET user_company_id = ? WHERE name = ?", (new_text, current_values[0],))
    database_manager.curs.execute("UPDATE insertdata SET user_company_id = ? WHERE name = ?", (new_text, current_values[0],))
    database_manager.conn.commit()
    update_label.configure(text="To make a full data change, user must log in again!", text_color=("#f09999"))
   else:
    database_manager.curs.execute("UPDATE registration SET class = ? WHERE user_company_id = ?", (new_text,current_values[1],))
    database_manager.conn.commit()
    update_label.configure(text="To make a full data change, user must log in again!", text_color=("#f09999"))

   event.widget.destroy()
