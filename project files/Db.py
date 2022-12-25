import sqlite3


class Db:
    def __init__(self, city: str):
        self.db = sqlite3.connect(f'{city}.db')
        self.cursor = self.db.cursor()

    def get_coordinates(self, street, house_number):
        self.cursor.execute(f"SELECT lat, lon FROM ways "
                            f"WHERE ([addr:street] = '{street} улица' "
                            f"OR [addr:street] = 'улица {street}' "
                            f"OR [addr:street] = '{street}') "
                            f"AND [addr:housenumber] = '{house_number}'")
        result = self.cursor.fetchall()
        return result

    def get_supposed_street_names(self, house_number):
        self.cursor.execute(f"SELECT [addr:street] FROM ways "
                            f"WHERE [addr:housenumber] = "
                            f"'{house_number}' ")
        results = self.cursor.fetchall()
        return results

    def get_coordinates_supposed_address(self, street, house_number):
        self.cursor.execute(f"SELECT lat, lon FROM ways "
                            f"WHERE [addr:street] = '{street}' "
                            f"AND [addr:housenumber] = '{house_number}'")
        result = self.cursor.fetchall()
        return result

    def get_nodes_by_way_id(self, way_id):
        self.cursor.execute(f"SELECT nodes FROM ways "
                            f"WHERE id = '{way_id}'")
        result = self.cursor.fetchall()
        return result

    def get_organizations_in_building_by_id_way(self, way_id):
        nodes = self.get_nodes_by_way_id(way_id)[0][0].split()
        lats_and_lons = []
        for node in nodes:
            lat_and_lon = self.get_lat_and_lon_by_node_id(node)[0]
            lats_and_lons.append(lat_and_lon)
        max_lat_and_lon = self.get_max_lat_and_lon_in_way(lats_and_lons)
        min_lat_and_lon = self.get_min_lat_and_lon_in_way(lats_and_lons)
        # print(max_lat_and_lon)
        # print(min_lat_and_lon)
        nodes_inside = self.get_nodes_inside_building(min_lat_and_lon,
                                                      max_lat_and_lon)
        result = []
        for node_inside in nodes_inside:
            # amenity = self.get_amenity_by_node_id(node_inside[0])[0][0]
            # shop = self.get_shop_by_node_id(node_inside[0])[0][0]
            # craft = self.get_craft_by_node_id(node_inside[0])[0][0]
            # if (amenity is not None or
            #         shop is not None or
            #         craft is not None):
            name = self.get_node_name_by_node_id(node_inside[0])[0][0]
            if name is not None:
                result.append(name)
        return result

    def get_id_way(self, street, house_number):
        self.cursor.execute(f"SELECT id FROM ways "
                            f"WHERE ([addr:street] = '{street} улица' "
                            f"OR [addr:street] = 'улица {street}' "
                            f"OR [addr:street] = '{street}') "
                            f"AND [addr:housenumber] = '{house_number}'")
        result = self.cursor.fetchall()
        return result

    def get_lat_and_lon_by_node_id(self, node_id):
        self.cursor.execute(f"SELECT lat, lon FROM nodes "
                            f"WHERE id = '{node_id}'")
        result = self.cursor.fetchall()
        return result

    def get_nodes_inside_building(self, min_lat_lon, max_lat_lon):
        self.cursor.execute(f"SELECT id FROM nodes "
                            f"WHERE (lat > '{min_lat_lon[0]}' "
                            f"AND lat < '{max_lat_lon[0]}' "
                            f"AND lon < '{min_lat_lon[1]}' "
                            f"AND lon > '{max_lat_lon[1]}')")
        result = self.cursor.fetchall()
        return result

    @staticmethod
    def get_min_lat_and_lon_in_way(lats_and_lons):
        min_lon = 1000
        min_lat = 1000
        for lat_and_lon in lats_and_lons:
            lat = lat_and_lon[0]
            lon = lat_and_lon[1]
            if lat < min_lat:
                min_lat = lat
                min_lon = lon
        return min_lat, min_lon

    @staticmethod
    def get_max_lat_and_lon_in_way(lats_and_lons):
        max_lon = -1000
        max_lat = -1000
        for lat_and_lon in lats_and_lons:
            lat = lat_and_lon[0]
            lon = lat_and_lon[1]
            if lat > max_lat:
                max_lat = lat
                max_lon = lon
        return max_lat, max_lon

    def get_amenity_by_node_id(self, node_id):
        self.cursor.execute(f"SELECT [amenity] FROM nodes "
                            f"WHERE id = '{node_id}'")
        result = self.cursor.fetchall()
        return result

    def get_shop_by_node_id(self, node_id):
        self.cursor.execute(f"SELECT [shop] FROM nodes "
                            f"WHERE id = '{node_id}'")
        result = self.cursor.fetchall()
        return result

    def get_craft_by_node_id(self, node_id):
        self.cursor.execute(f"SELECT [craft] FROM nodes "
                            f"WHERE id = '{node_id}'")
        result = self.cursor.fetchall()
        return result

    def get_node_name_by_node_id(self, node_id):
        self.cursor.execute(f"SELECT [name] FROM nodes "
                            f"WHERE id = '{node_id}'")
        result = self.cursor.fetchall()
        return result