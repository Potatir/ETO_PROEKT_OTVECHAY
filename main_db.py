import requests
import psycopg2
import time
from datetime import datetime


API_KEY = '8e9cf68cbd7790771fedf34c66c97c9f'
CITY = 'Astana'
name = 'main'

def create_table():
    connection = psycopg2.connect(database = 'postgres', user = 'postgres', password = '1234567', port = '5432')
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS weather_data (
            id SERIAL PRIMARY KEY,
            date_ date,
            temperature REAL
        )
    ''')

    connection.commit()
    connection.close()

def reset_table():
    connection = psycopg2.connect(database = 'postgres', user = 'postgres', password = '1234567', port = '5432')
    cursor = connection.cursor()

    cursor.execute('DROP TABLE IF EXISTS weather_data')
    create_table()

    connection.commit()
    connection.close()

def insert_data(date_, temperature):
    connection = psycopg2.connect(database = 'postgres', user = 'postgres', password = '1234567', port = '5432')
    cursor = connection.cursor()

    cursor.execute('INSERT INTO weather_data (date_, temperature) VALUES (%s, %s)', (date_, temperature))

    connection.commit()
    connection.close()

def get_weather_data(api_key, city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(url)
    data = response.json()

    temperature = data['main']['temp']
    date_ = time.strftime('%Y-%m-%d')

    return date_, temperature

if name == 'main':
    create_table()

    current_month = datetime.now().month

    while True:
        date_, temperature = get_weather_data(API_KEY, CITY)

        if datetime.now().month != current_month:
            reset_table()
            current_month = datetime.now().month

        insert_data(date_, temperature)

        time.sleep(24 * 60 * 60)
