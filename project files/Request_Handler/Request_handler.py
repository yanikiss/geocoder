
class RequestHandler:
    def __init__(self, city: str, street_name: str):
        self.city = city
        self.street = street_name
        self.city_options = []
        self.street_options = []

        with open('Request_Handler/City_handler.txt', 'r') as f:
            for option in f:
                option = option.replace('\n', '')
                self.city_options.append(option)
            f.close()

        with open('Request_Handler/Street_handler.txt', 'r') as f:
            for option in f:
                option = option.replace('\n', '')
                self.street_options.append(option)
            f.close()

        self.do_processing_street()
        self.do_processing_city()

    def do_processing_city(self):
        if len(self.city.strip().split()) > 1:
            start_city_name = self.city.split()[0].lower()
            if start_city_name in self.city_options:
                self.city = self.city.replace(start_city_name, '', 1)
                self.city = self.city.strip()
        self.city = self.city[0].upper() + self.city[1:]

    def do_processing_street(self):
        if len(self.street.strip().lower().split()) > 1:
            start_street_name = self.street.strip().lower().split()[0]
            if start_street_name in self.street_options:
                self.street = self.street.replace(start_street_name, '', 1)
                self.street = self.street.strip()


