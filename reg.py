from customtkinter import *
from tkinter import messagebox
from db_manager import *

def user_reg():
    log = CTkToplevel()
    log.grab_set()
    log.title("Registration")
    log.geometry('500x500')
    set_appearance_mode("light")
    log.resizable(False, False)

    reg_label = CTkLabel(log, text="Registration", font=("Arial", 30))
    name_label = CTkLabel(log, text="Name", font=("Arial", 16, 'bold'))
    reg_id_label = CTkLabel(log, text="User ID", font=("Arial", 16, 'bold'))
    reg_email_label = CTkLabel(log, text="Email", font=("Arial", 16, 'bold'))
    reg_password_label = CTkLabel(log, text="Password", font=("Arial", 16, 'bold'))
    reg_name_entry = CTkEntry(log, font=("Arial", 16))
    reg_id_entry = CTkEntry(log, font=("Arial", 16))
    reg_email_entry = CTkEntry(log, font=("Arial", 16))
    reg_password_entry = CTkEntry(log, show="*", font=("Arial", 16))
    reg_button = CTkButton(log, text="Registration", font=("Arial", 16), command=lambda: registration(reg_name_entry, reg_id_entry, reg_email_entry, reg_password_entry, messagebox, log))

    reg_label.place(relx=0.5, rely=0.2, anchor="center")
    name_label.place(relx=0.3, rely=0.3, anchor="center")
    reg_id_label.place(relx=0.3, rely=0.4, anchor="center")
    reg_email_label.place(relx=0.3, rely=0.5, anchor="center")
    reg_password_label.place(relx=0.3, rely=0.6, anchor="center")
    reg_name_entry.place(relx=0.6, rely=0.3, anchor="center")
    reg_id_entry.place(relx=0.6, rely=0.4, anchor="center")
    reg_email_entry.place(relx=0.6, rely=0.5, anchor="center")
    reg_password_entry.place(relx=0.6, rely=0.6, anchor="center")
    reg_button.place(relx=0.5, rely=0.7, anchor="center")

    log.mainloop()