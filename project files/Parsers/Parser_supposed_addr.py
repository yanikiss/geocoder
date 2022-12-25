import Calcucator_distance


class Parser:
    @staticmethod
    def get_addr(db, street: str, house_number: str) -> list:
        supposed_addr = []
        street = street.lower()

        supposed_streets = db.get_supposed_street_names(house_number)
        results = [str(x[0]) for x in supposed_streets]

        calculator = Calcucator_distance.Calculator()
        for result in results:
            if result is not None:
                l_distance1 = calculator.calculate_distance(f'{street} улица',
                                                            result)
                l_distance2 = calculator.calculate_distance(f'улица {street}',
                                                            result)
                l_distance3 = calculator.calculate_distance(street, result)

                if l_distance1 <= 3 or l_distance2 <= 3 or l_distance3 <= 3:
                    supposed_street = result
                    supposed_addr.append(supposed_street)
                    supposed_addr.append(house_number)
                    break
        return supposed_addr