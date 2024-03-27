from customtkinter import *
from tkinter import ttk
from config import DatabaseManager

database_manager = DatabaseManager()
edit_profile_table = None

def edit_profile(fetched_id):

    #profil szerkesztő ablak/regisztrációs ablak

    global edit_profile_table
    edit = CTkToplevel()
    edit.grab_set()
    edit.title("Registration")
    edit.geometry('500x500')
    set_appearance_mode("light")
    edit.resizable(False, False)

    #edit gomb hozzáadása a frame-hez
    
    edit_profile_edit_profile_table_frame = CTkFrame(edit)
    edit_profile_edit_profile_table_frame.place(x=3, y=50)
    
    #oszlop címezése
    
    cols = ("Name", "ID", "Class")
    edit_profile_table = ttk.Treeview(edit_profile_edit_profile_table_frame, columns=cols, height=12)
    scrollbar = CTkScrollbar(edit_profile_edit_profile_table_frame, command=edit_profile_table.yview)

    #oszlopok elhelyezése, berendezése 
    
    for col in cols:
      edit_profile_table.heading(col, text=col, anchor='center')
      edit_profile_table.column(col, width=154, anchor="center")
      edit_profile_table.column("#0", width=28, anchor="ne")
    edit_profile_table.pack(side="left", fill="y")
    edit_profile_table.configure(yscrollcommand=scrollbar.set)
    get_data()    

    del_member = CTkButton(edit, text="Delete member", command=lambda:delete_member(fetched_id, edit))
    del_member.place(x=190, y=350)

    edit.mainloop()


def get_data():
   
   #sql query: fetch, adat kijelölése
   
   database_manager.curs.execute("SELECT name, user_company_id, class FROM registration")
   datas = database_manager.curs.fetchall()
   edit_profile_table.delete(*edit_profile_table.get_children())

   #adatbázis hiányos adatainak feltöltése NULL-al

   for i, data in enumerate(datas):
    clean_data = ["" if d is None else d for d in data]
    edit_profile_table.insert("", "end",values=(clean_data[0], clean_data[1], clean_data[2]))


def delete_member(fetched_id, win):

    #tag törlés függvény

   notapproved_delete_member = CTkLabel(win, text="", font=("Arial", 14, "bold"))
   notapproved_delete_member.pack()
   item = edit_profile_table.selection()
   values = edit_profile_table.item(item, "values")
 
   #sql sor törlése és adatbázis frissítése
   database_manager.curs.execute("DELETE FROM registration WHERE user_company_id = ? AND NOT user_company_id= ?", (values[1], fetched_id,))
   database_manager.conn.commit()
   
   #hibakezelés arra, ha bizonyos tagokat engedély nélkül akarnak törölni

   if fetched_id == values[1]:
      notapproved_delete_member.configure(text="This member cannot be deleted!", text_color=("#f09999"))
   get_data()