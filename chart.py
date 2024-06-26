from customtkinter import *
from config import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import numpy as np
database_manager = DatabaseManager()


def chart_frame(win, fetched_id):
    #Tkinter Frame létrehozása és elhelyezése
    chart_filter_frame = CTkFrame(win, width=550, height=300, border_width=3, fg_color=("#edebeb"))
    chart_filter_frame.place(x=845, y=5)
    #Button és Option gomb lérehozása, elhelyezése
    type_filter_omenu= CTkOptionMenu(chart_filter_frame, values=["Overtime", "Standby", "Sliding"])
    filter_set_button = CTkButton(chart_filter_frame, text="Set", command= lambda: filter(type_filter_omenu, chart_filter_frame, fetched_id))
    type_filter_omenu.place(relx=0.35, rely=0.85)
    filter_set_button.place(relx=0.65, rely=0.85)
    
def filter(type,  win, id):
    #Ha nem kapt típusbeli bevitelt akkor return
    if not type.get():
        return
    #A chart lokális változói
    months = ["Jan", "Feb", "Már", "Ápr", "Máj", "Jún", "Júl", "Aug", "Szep", "Okt", "Nov", "Dec"]
    approved_day = 0
    approved_hour = 0
    approved_full_time = 0
    approved_full_times = [0] * len(months)
    not_approved_full_times = [0] * len(months)
    #DB lekérés
    database_manager.curs.execute("SELECT counted_day, counted_hour, counted_min, month, approval FROM  insertdata WHERE user_company_id = ? AND type = ?", (id, type.get(),))
    datas = database_manager.curs.fetchall()
    #A lekért adatok végig iterálása és a lokális változók feltöltése
    for i in range(len(datas)):
        if datas[i][4] == 1 and datas[i][3][0:3] in months:
            month_index = months.index(datas[i][3][0:3])
            approved_day = datas[i][0]
            approved_hour = datas[i][1]
            approved_full_time = (approved_day * 24) + approved_hour
            approved_full_times[month_index] += approved_full_time
        elif datas[i][4] == 0 and datas[i][3][0:3] in months:
            month_index = months.index(datas[i][3][0:3])
            approved_day = datas[i][0]
            approved_hour = datas[i][1]
            approved_full_time = (approved_day * 24) + approved_hour
            not_approved_full_times[month_index] += approved_full_time
    #A chart feltöltése a lokális változók tartalmával    
    chart(win, type.get(), months, approved_full_times, not_approved_full_times)


    
def chart(frame_win, type, months, approved_full_times, not_approved_full_times):
    #A chart elfogadott és nem elfogadott adatai incializálása
    approve_counts = {
                        '1': np.array(approved_full_times),
                        '0': np.array(not_approved_full_times),
                    }
    #A chart design incializálása
    fig, ax = plt.subplots(figsize=(20, 10))
    bottom = np.zeros(len(months))
    colors = {'1': '#d1facf', '0': '#f7adad'}
    #Lekért adatok végigi iterálása és elhelyezése a chart-on
    for lab,count in approve_counts.items():
        p = ax.bar(months, count, width=0.8, label=lab, bottom=bottom, color=colors[lab], linewidth=0.2)
        bottom += count

        ax.bar_label(p, label_type='center')

    ax.set_title(type)
    ax.legend()
    #Chart létrehozása és elhelyezése a szülő Frame-en
    canvas = FigureCanvasTkAgg(fig, master=frame_win)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.place(relx=0.05, rely=0.1, width=500, height=200)
    canvas.draw()
