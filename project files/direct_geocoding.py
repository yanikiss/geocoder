import sqlite3


class Geocoder:
    def __init__(self, city, street, house_number):
        self.city = city
        self.street = street
        self.house_number = house_number

    def do_geocoding(self):
        db = sqlite3.connect(f'{self.city}.db')
        cursor = db.cursor()
        cursor.execute(f"SELECT lat, lon FROM ways "
                       f"WHERE ([addr:street] = '{self.street} улица' "
                       f"OR [addr:street] = 'улица {self.street}') "
                       f"AND [addr:housenumber] = '{self.house_number}'")
        result = cursor.fetchall()
        print('Your coordinates:')
        print(str(result[0][0]) + ',', result[0][1])
