import Parsers.Parser_supposed_addr as Supposed_address_parser


class Geocoder:
    def __init__(self, city: str, street: str, house_number: str,
                 org_flag: str, db=None):
        self.street = street
        self.city = city
        self.house_number = house_number
        self.org_flag = org_flag
        self.db = db

    def do_geocoding(self):
        coordinates = self.db.get_coordinates(self.street, self.house_number)
        way_id = self.db.get_id_way(self.street, self.house_number)[0][0]
        if len(coordinates) != 0:
            print('\nВаши координаты:')
            print(f"широта={coordinates[0][0]}, долгота={coordinates[0][1]}")
            if self.org_flag == 'да':
                organizations = self.db.get_organizations_in_building_by_id_way(way_id)
                if len(organizations != 0):
                    print('В этом здании есть:')
                    for organization in organizations:
                        print(organization.replace('\'', ''))
                else:
                    print('В этом здании нет организаций')
            return

        supposed_address = Supposed_address_parser. \
            Parser.get_addr(self.db,
                            self.street,
                            self.house_number)
        if len(supposed_address) != 0:
            supposed_street = supposed_address[0]
            numb_result = supposed_address[1]
            print(f'Идет поиск по адресу: {supposed_street} {numb_result}')

            supposed_coordinates = self.db.get_coordinates_supposed_address(
                supposed_street, numb_result)

            print('\nВаши координаты:')
            print(f"долгота= {supposed_coordinates[0][0]}, "
                  f"широта= {supposed_coordinates[0][1]}")
            if self.org_flag == 'да':
                pass
        else:
            print('Этот адрес не найден. '
                  '\nПроверьте, что введенные даннеы верны, и попробуйте еще раз.')



# if self.street == 'сулимова' and self.house_number == '42':
#     cursor.execute(f"SELECT * FROM ways "
#                    f"WHERE id = 37285726")
#     res1 = list(cursor.fetchall()[0])
#     ress1 = []
#     for i in res1:
#         if i is not None:
#             ress1.append(i)
#     print(ress1)
#     cursor.execute(f"SELECT * FROM ways "
#                    f"WHERE id = 46906736")
#     res2 = list(cursor.fetchall()[0])
#     ress2 = []
#     for i in res2:
#         if i is not None:
#             ress2.append(i)
#     print(ress2)
#     return