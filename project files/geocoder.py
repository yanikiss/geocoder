import os
import parser
import sqlite3
import requests
import direct_geocoding

print('Hello! This is an application for geocoding addresses of Russia \n'
      'Please enter city\n', end='>>>')
city = input()
print('Enter street name\n', end='>>>')
street = input()
print('Enter house number\n', end='>>>')
house_number = input()

file_name_db = city + '.db'
geocoder = direct_geocoding.Geocoder(city, street, house_number)
if os.path.isfile(file_name_db):
    geocoder.do_geocoding()
else:
    db = sqlite3.connect('cities.db')
    cursor = db.cursor()
    cursor.execute(f"SELECT west, south, east, north FROM cities WHERE city = '{city}'")
    w_s_e_n = cursor.fetchall()[0]
    if len(w_s_e_n) == 0:
        print('This city is not in the database')
    w, s, e, n = w_s_e_n[0], w_s_e_n[1], w_s_e_n[2], w_s_e_n[3]
    response = requests.get(f'https://overpass-api.de/api/map?bbox={w},{s},{e},{n}')
    with open(f'./{city}.xml', 'wb') as f:
        for chunk in response.iter_content(chunk_size=10 * 1024 * 1024):
            if chunk:
                f.write(chunk)
    parser = parser.Parser(city)
    parser.parse_xml(f'./{city}.xml')
    geocoder.do_geocoding()

