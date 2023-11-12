from tkinter import *
from tkinter import ttk
import psycopg2
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import traceback

class Appwin:
    def __init__(self):
        try:
            self.win = Tk()
            self.win.grid()
            self.update_button = ttk.Button(self.win, text="Обновить график", command=self.update_graph)
            self.update_button.grid(row=0, column=0, padx=8, pady=8)
            self.canvas = None  
            self.graph()  
            self.win.mainloop()
        except:
            print("Не получилось создать окно")
    def get_data(self):
        try:
            self.conn = psycopg2.connect(database = 'postgres', user = 'postgres', password = '222222', port = '5432')
            self.cur = self.conn.cursor()
            self.cur.execute("SELECT temperature FROM weather_data")
            self.data = self.cur.fetchall()
            self.conn.close()
            return(self.data)
        except ConnectionError:
            print("не удалось подключиться к бд")
    def graph(self):
        try:
            self.conn = psycopg2.connect(database = 'postgres', user = 'postgres', password = '222222', port = '5432')
            self.cur = self.conn.cursor()
            self.cur.execute("SELECT date_ FROM weather_data")
            self.date = self.cur.fetchall()
            self.conn.close()
            self.data = self.get_data()
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.plot(self.date, self.data, label="График данных")

            ax.set_xlabel("Время")
            ax.set_ylabel("Значение")
            ax.legend()
            if self.canvas:
                self.canvas.get_tk_widget().destroy()

            self.canvas = FigureCanvasTkAgg(fig, master=self.win)
            self.canvas_widget = self.canvas.get_tk_widget()
            self.canvas_widget.grid(row=5, column=0, padx=5, pady=5)
        except Exception:
            traceback.print_exc()
    def update_graph(self):
        self.graph()

        






first = Appwin()