from customtkinter import *
from reg import *
from db_manager import *

def login_ui():
  app = CTk()
  app.title("Login employee manager")
  app.geometry('750x550')
  set_appearance_mode("light")
  app.resizable(False, False)

  login_label = CTkLabel(app, text="Login", font=("Arial", 30))
  email_label = CTkLabel(app, text="Email", font=("Arial", 16, 'bold'))
  password_label = CTkLabel(app, text="Password", font=("Arial", 16, 'bold'))
  email_entry = CTkEntry(app, font=("Arial", 16))
  password_entry = CTkEntry(app, show="*", font=("Arial", 16))
  login_button = CTkButton(app, text="Login", font=("Arial", 16), command=lambda: login(email_entry, password_entry, app))
  reg_button = CTkButton(app, text="Registration", font=("Arial", 16), command=user_reg)

  login_label.place(relx=0.5, rely=0.3, anchor="center")
  email_label.place(relx=0.4, rely=0.4, anchor="center")
  email_entry.place(relx=0.6, rely=0.4, anchor="center")
  password_label.place(relx=0.4, rely=0.5, anchor="center")
  password_entry.place(relx=0.6, rely=0.5, anchor="center")
  login_button.place(relx=0.4, rely=0.6, anchor="center")
  reg_button.place(relx=0.6, rely=0.6, anchor="center")

  app.mainloop()