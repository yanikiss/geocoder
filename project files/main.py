import os
from Parsers import Parser_xml
import sqlite3
import requests
import Direct_geocoding
from Request_Handler import Request_handler
import Db

print('Привет! Эта утилита для геокодирования адресов больших городов России \n'
      'Введите название города\n', end='>>>')
city = input().strip()
print('Введите название улицы\n', end='>>>')
street = input().strip()
print('Введите номер дома\n', end='>>>')
house_number = input().strip()
print('Вывести список организаций в здании? [да/нет]\n', end='>>>')
org_flag = input().strip()

req_handler = Request_handler.RequestHandler(city, street)
geocoder = Direct_geocoding.Geocoder(req_handler.city, req_handler.street,
                                     house_number, org_flag)
file_name_db = geocoder.city + '.db'
if os.path.isfile(file_name_db):
    geocoder.db = Db.Db(geocoder.city)
    geocoder.do_geocoding()
else:
    db = sqlite3.connect('cities.db')
    cursor = db.cursor()
    cursor.execute(f"SELECT west, south, east, north FROM cities "
                   f"WHERE city = '{geocoder.city}'")
    w_s_e_n = cursor.fetchall()
    if len(w_s_e_n) == 0:
        print('This city is not in the database')
        print(geocoder.city)
    else:
        w_s_e_n = w_s_e_n[0]
        w, s, e, n = w_s_e_n[0], w_s_e_n[1], w_s_e_n[2], w_s_e_n[3]
        response = requests.get(f'https://overpass-api.de/api/map?'
                                f'bbox={w},{s},{e},{n}')
        with open(f'./{geocoder.city}.xml', 'wb') as f:
            for chunk in response.iter_content(chunk_size=10 * 1024 * 1024):
                if chunk:
                    f.write(chunk)
        f.close()
        parser = Parser_xml.Parser(geocoder.city)
        parser.parse_xml(f'./{geocoder.city}.xml')

        geocoder.db = Db.Db(geocoder.city)
        geocoder.do_geocoding()

