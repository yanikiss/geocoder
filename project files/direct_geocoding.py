import sqlite3


def distance(a, b):
    n, m = len(a), len(b)
    if n > m:
        a, b = b, a
        n, m = m, n
    current_row = range(n + 1)
    for i in range(1, m + 1):
        previous_row, current_row = current_row, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete, change = previous_row[j] + 1, \
                                  current_row[j - 1] + 1, previous_row[j - 1]
            if a[j - 1] != b[i - 1]:
                change += 1
            current_row[j] = min(add, delete, change)
    return current_row[n]


class Geocoder:
    def __init__(self, city: str, street: str, house_number: str):
        street = street.lower()
        if 'улица' in street:
            street = street.replace('улица', '')
        elif 'ул.' in street:
            street = street.replace('ул.', '')
        elif 'ул' in street:
            street = street.replace('ул', '')
        self.street = street.strip()

        if len(city.split()) > 1:
            g = city.split()[0]
            if (g.lower() == 'г' or g.lower() == 'г.' or g == 'город'
                    or g == 'Город' or g == 'гор.' or g == 'гор'
                    or g == 'Гор' or g == 'Гор.'):
                city = city.replace(g, '')
                city = city.strip()
        self.city = city[0].upper() + city[1:]

        self.house_number = house_number

    def do_geocoding(self):
        db = sqlite3.connect(f'{self.city}.db')
        cursor = db.cursor()
        cursor.execute(f"SELECT lat, lon FROM ways "
                       f"WHERE ([addr:street] = '{self.street} улица' "
                       f"OR [addr:street] = 'улица {self.street}' "
                       f"OR [addr:street] = '{self.street}') "
                       f"AND [addr:housenumber] = '{self.house_number}'")
        result = cursor.fetchall()
        if len(result) != 0:
            print('Your coordinates:')
            print(str(result[0][0]) + ',', result[0][1])
            return
        supposed_street = ''
        cursor.execute(f"SELECT [addr:street] FROM ways "
                       f"WHERE [addr:housenumber] = '{self.house_number}' ")
        results = cursor.fetchall()
        results = [str(x[0]) for x in results]
        for result in results:
            if result is not None:
                l_distance1 = distance(self.street + ' улица', result)
                l_distance2 = distance('улица ' + self.street, result)
                numb_street_name = self.street[::-1]
                numbers = [str(x) for x in range(0, 10)]
                for n in numb_street_name:
                    if n not in numbers:
                        numb_street_name = numb_street_name.replace(n, '')
                numb_result = ''
                for r in result:
                    if r in numbers:
                        numb_result += r
                if (l_distance1 <= 3 or l_distance2 <= 3
                        and numb_result == numb_street_name):
                    self.street = result
                    break
                if (4 <= l_distance1 <= 6 or 4 <= l_distance2 <= 6
                        or (l_distance1 <= 3 or l_distance2 <= 3
                            and numb_result != numb_street_name)):
                    supposed_street = result
        cursor.execute(f"SELECT lat, lon FROM ways "
                       f"WHERE [addr:street] = '{self.street}' "
                       f"AND [addr:housenumber] = '{self.house_number}'")
        result = cursor.fetchall()
        if len(result) == 0:
            print('This address was not found. '
                  '\nCheck if the input data is correct and try again.')
            if supposed_street == '':
                print(f"Maybe you mean {supposed_street} {self.house_number}?")
        else:
            print('\nYour coordinates:')
            print(str(result[0][0]) + ',', result[0][1])
