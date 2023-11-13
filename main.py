from tkinter import *
from tkinter import ttk
import requests
import traceback

class Appwin:
    def __init__(self, api_key, city):
        self.API_KEY = api_key
        self.CITY = city

        self.win = Tk()
        self.win.title("Weather App")
        self.win.geometry("300x200")

        self.update_button = ttk.Button(self.win, text="Обновить график", command=self.update_weather_widgets)
        self.update_button.pack(pady=10)

        self.temperature_label = ttk.Label(self.win, text="Температура:")
        self.temperature_label.pack(pady=5)

        self.humidity_label = ttk.Label(self.win, text="Влажность:")
        self.humidity_label.pack(pady=5)

        self.wind_speed_label = ttk.Label(self.win, text="Скорость ветра:")
        self.wind_speed_label.pack(pady=5)

        self.pressure_label = ttk.Label(self.win, text="Давление:")
        self.pressure_label.pack(pady=5)

        self.update_weather_widgets()
        self.win.mainloop()

    def get_weather_data(self):
        try:
            url = f'http://api.openweathermap.org/data/2.5/weather?q={self.CITY}&appid={self.API_KEY}&units=metric'
            response = requests.get(url)
            data = response.json()

            temperature = data['main']['temp']
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']
            pressure = data['main']['pressure']

            return temperature, humidity, wind_speed, pressure

        except Exception:
            traceback.print_exc()

    def update_weather_widgets(self):
        try:
            temperature, humidity, wind_speed, pressure = self.get_weather_data()

            self.temperature_label.config(text=f"Температура: {temperature} °C")
            self.humidity_label.config(text=f"Влажность: {humidity}%")
            self.wind_speed_label.config(text=f"Скорость ветра: {wind_speed} м/с")
            self.pressure_label.config(text=f"Давление: {pressure} мм рт. ст.")

        except Exception:
            traceback.print_exc()

if __name__ == "__main__":
    api_key = '8e9cf68cbd7790771fedf34c66c97c9f'
    city = 'Astana'
    first = Appwin(api_key, city)
