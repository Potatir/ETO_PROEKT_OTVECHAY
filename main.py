from tkinter import *
from tkinter import ttk
import psycopg2
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import traceback
import requests
from datetime import datetime

class Appwin:
    def __init__(self):
        try:
            self.win = Tk()
            self.win.attributes('-fullscreen', True)

            style = ttk.Style()
            style.configure("TLabel", font=("Arial", 16))
            self.current_date_label = ttk.Label(self.win, text="Дата: ")
            self.current_date_label.grid(row=1, column=0, padx=8, pady=8, sticky="w")
            self.current_city_label = ttk.Label(self.win, text="Город: ")
            self.current_city_label.grid(row=2, column=0, padx=8, pady=8, sticky="w")
            self.current_temp_label = ttk.Label(self.win, text="Температура: ")
            self.current_temp_label.grid(row=1, column=2, padx=8, pady=8, sticky="e")
            self.weather_condition_label = ttk.Label(self.win, text="Состояние погоды: ")
            self.weather_condition_label.grid(row=2, column=2, padx=8, pady=8, sticky="e")

            self.update_button = ttk.Button(self.win, text="Обновить график", command=self.update_graph)
            self.update_button.grid(row=0, column=1, padx=8, pady=8)

            self.canvas = None
            self.graph()
            self.update_weather_info() 
            self.win.mainloop()
        except:
            print("He получилось создать окно")

    def update_weather_info(self):
        try:
            api_key = '8e9cf68cbd7790771fedf34c66c97c9f'
            city = 'Astana' 
            url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'

            response = requests.get(url)
            data = response.json()
            current_date_timestamp = data['dt']
            current_city = data['name']
            current_temp_kelvin = data['main']['temp']
            weather_condition_code = data['weather'][0]['id']

            current_date = datetime.utcfromtimestamp(current_date_timestamp).strftime('%d:%m:%Y')

            current_temp_celsius = round(current_temp_kelvin - 273.15, 2)

            weather_condition_translation = self.translate_weather_condition(weather_condition_code)

            self.current_date_label.config(text=f"Дата: {current_date}")
            self.current_city_label.config(text=f"Город: {current_city}")
            self.current_temp_label.config(text=f"Температура: {current_temp_celsius}°C")
            self.weather_condition_label.config(text=f"Состояние погоды: {weather_condition_translation}")
        except Exception as e:
            print(f"Error updating weather information: {e}")

    def translate_weather_condition(self, condition_code):
        translation_dict = {
            200: "гроза c небольшим дождем",
            201: "гроза c дождем",
            202: "гроза c проливным дождем",
            210: "небольшая гроза",
            211: "гроза",
            212: "сильная гроза",
            221: "гроза",
            230: "гроза c легким моросящим дождем",
            231: "гроза c моросящим дождем",
            232: "гроза c проливным моросящим дождем",
            300: "легкий моросящий дождь",
            301: "моросящий дождь",
            302: "проливной дождь",
            310: "легкий моросящий дождь",
            311: "моросящий дождь",
            312: "проливной дождь",
            313: "дождь и легкий моросящий дождь",
            314: "дождь и моросящий дождь",
            321: "проливной дождь",
            500: "легкий дождь",
            501: "умеренный дождь",
            502: "сильный дождь",
            503: "очень сильный дождь",
            504: "крайне сильный дождь",
            511: "ледяной дождь",
            520: "легкий проливной дождь",
            521: "проливной дождь",
            522: "сильный проливной дождь",
            531: "проливной дождь",
            600: "легкий снег",
            601: "снег",
            602: "сильный снегопад",
            611: "мокрый снег",
            612: "дождь co снегом",
            613: "снегопад",
            615: "легкий дождь co снегом",
            616: "дождь co снегом",
            620: "легкий снегопад",
            621: "снегопад",
            622: "сильный снегопад",
            701: "туман",
            711: "дым",
            721: "мгла",
            731: "песок/пыль",
            741: "туман",
            751: "песок",
            761: "пыль",
            762: "вулканический пепел",
            771: "шквал",
            781: "торнадо",
            800: "ясно",
            801: "малооблачно",
            802: "переменная облачность",
            803: "переменная облачность",
            804: "пасмурно"
        }
        return translation_dict.get(condition_code, "Неизвестно")

    def get_data(self):
        try:
            self.conn = psycopg2.connect(database='postgres', user='postgres', password='222222', port='5432')
            self.cur = self.conn.cursor()
            self.cur.execute("SELECT temperature FROM weather_data")
            self.data = self.cur.fetchall()
            self.conn.close()
            return self.data
        except ConnectionError:
            print("не удалось подключиться к бд")

    def graph(self):
        try:
        
            self.conn = psycopg2.connect(database='postgres', user='postgres', password='222222', port='5432')
            self.cur = self.conn.cursor()
            self.cur.execute("SELECT date_ FROM weather_data")
            self.date = self.cur.fetchall()
            self.conn.close()
            self.data = self.get_data()
            fig, ax = plt.subplots(figsize=(14, 10))
            ax.plot(self.date, self.data, label="График данных")

            ax.set_xlabel("Дата")
            ax.set_ylabel("Температура")
            ax.legend()
            ax.tick_params(axis='x', rotation=45)  
            ax.axes.get_xaxis().set_visible(False)

            if self.canvas:
                self.canvas.get_tk_widget().destroy()

            self.canvas = FigureCanvasTkAgg(fig, master=self.win)
            self.canvas_widget = self.canvas.get_tk_widget()
            self.canvas_widget.grid(row=1, column=1, rowspan=2, padx=5, pady=5, sticky="nsew")  

        except Exception:
            traceback.print_exc()

    def update_graph(self):
        self.graph()
        self.update_weather_info()  


first = Appwin()
