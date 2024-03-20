import psycopg2
from config import *
from datetime import datetime
from customtkinter import *
from config import DatabaseManager
from progressbar import *
from save_data import *


database_manager = DatabaseManager()

def registration(name, uid, email, password, message, win):
    try:
        if not name.get() and not uid.get() and not email.get() and not password.get():
            win.destroy()
            message.showerror(title="Registration error", message="Fields are mandatory")
            return

        database_manager.curs.execute("INSERT INTO registration (user_company_id, email_address, password, name, class, permission) VALUES (?, ?, ?, ?, ?, ?)", (uid.get(), email.get(), password.get(), name.get(), "F", 0))
        database_manager.conn.commit()
        name.delete(0, 'end')
        uid.delete(0, 'end')
        email.delete(0, 'end')
        password.delete(0, 'end')
        message.showinfo(title="Registration", message="Successfully registered! You can now log in!")
        win.destroy()
    except psycopg2.Error as e:
        message.showinfo(title="Failed to registration", message=f"Failed in registration, PostgreSQL error: {e}")
        win.destroy()
        return
    
def login(email, password, win):
    today = datetime.now()
    login_label = CTkLabel(win, text="", font=("Arial", 14, "bold"))
    login_label.place(x=320, y=440)
    
    if not email.get() and not password.get():
            login_label.configure(text="Field is mandantory!", text_color=("#f09999"))
            return

    database_manager.curs.execute("SELECT * FROM registration WHERE email_address = ? AND password = ?", (email.get(), password.get(),))
    datas = database_manager.curs.fetchall()
    
    if  datas:
        myValc = IntVar()
        progressbar = CTkProgressBar(win, orientation="horizontal", width=150, height=15, mode="determinate", determinate_speed=1, variable=myValc)
        progressbar.place(x=320, y=420)
        login_label.configure(text=f"{database_manager.connecting}", font=("Arial", 12))
        configure_progressbar(progressbar)

        database_manager.curs.execute("UPDATE registration SET permission = true, last_login = ? WHERE email_address = ?", (today, email.get(),))
        database_manager.conn.commit()
        win.destroy()
        save_data()
    else:
        login_label.configure(text="Invalid login.", text_color=("#f09999"))
        #message.showerror(title="Error", message="Invalid login.")
        email.delete(0, 'end')
        password.delete(0, 'end')