import xml.etree.ElementTree as ET
import os
import sqlite3
from tqdm import tqdm
import pickle


class Parser:
    def __init__(self, city):
        self.db = sqlite3.connect(city + '.db')
        self.cursor = self.db.cursor()
        self.id_nodes2lat_lon = {}

    def parse_xml(self, xml_file_location):
        node_tags = set()
        way_tags = set()

        tree = ET.iterparse(xml_file_location)
        file_name = "./node_way_tags.pickle"

        print('Creating and loading the database...Please, wait 1 minute')
        c = 0
        for event, elem in tree:
            c += 1
            if elem.tag == 'node':
                self.id_nodes2lat_lon[elem.attrib['id']] = [
                    float(elem.attrib['lat']), float(elem.attrib['lon'])]
                for tag in list(elem):
                    key = tag.attrib['k'].lower()
                    if key not in ['id', 'lat', 'lon']:
                        node_tags.add(key)
            elif elem.tag == 'way':
                children = list(elem)
                for child in children:
                    if child.tag == 'tag':
                        key = child.attrib['k'].lower()
                        if key not in ['id', 'nodes']:
                            way_tags.add(key)

        #     print('saving data...', end='', flush=True)
        #     with open(file_name, 'wb') as f:
        #         pickle.dump({'node': node_tags, 'way': way_tags,
        #                      'lat_lon': self.id_nodes2lat_lon}, f)
        #     print('done')
        # else:
        #     with open(file_name, 'rb') as f:
        #         data = pickle.load(f)
        #         node_tags = data['node']
        #         way_tags = data['way']
        #         self.id_nodes2lat_lon = data['lat_lon']
        #     print('data loaded')

        # ФОРМИРОВАНИЕ СТОЛБЦОВ В ТАБЛИЦАХ

        node_fields = ''
        for tag in node_tags:
            node_fields += f', [{tag}] TEXT'
        way_fields = ''
        for tag in way_tags:
            way_fields += f', [{tag}] TEXT'

        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS nodes "
                            f"(id INTEGER,"
                            f"lat DOUBLE,"
                            f"lon DOUBLE"
                            f"{node_fields})")
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS ways "
                            f"(id INTEGER,"
                            f"lat DOUBLE,"
                            f"lon DOUBLE,"
                            f"nodes TEXT"
                            f"{way_fields})")

        del tree
        new_tree = ET.iterparse(xml_file_location)

        # ЗАПОЛНЕНИЕ БАЗЫ
        for event, elem in new_tree:
            if elem.tag == 'node':
                self.parse_node(elem)
            if elem.tag == 'way':
                self.parse_way(elem)
        print('Done')

        self.cursor.execute(f"CREATE INDEX IF NOT EXISTS "
                            f"street_and_housenumber_idx "
                            f"ON ways ([addr:street], [addr:housenumber])")
        self.cursor.execute(f"CREATE INDEX IF NOT EXISTS "
                            f"id_lat_and_lon_idx "
                            f"ON nodes (id, lat, lon)")

        self.db.commit()
        os.remove(xml_file_location)

    def parse_node(self, elem):
        tags = list(elem)
        attributes = elem.attrib
        keys = ['id', 'lat', 'lon']
        values = [attributes['id'], attributes['lat'], attributes['lon']]
        for tag in tags:
            key = tag.attrib['k'].lower()
            value = tag.attrib['v']
            keys.append(key)
            values.append(value)
        self.fill_row(keys, values, 'nodes')

    def parse_way(self, elem):
        children = list(elem)
        attributes = elem.attrib
        nodes = set()
        keys = ['id', 'lat', 'lon', 'nodes']
        values = [attributes['id'], 0, 0, '']
        for child in children:
            if child.tag == 'nd':
                child_id = child.attrib['ref']
                nodes.add(child_id)
                values[3] += f'{child_id} '
            elif child.tag == 'tag':
                key = child.attrib['k'].lower()
                value = child.attrib['v'].lower()
                keys.append(key)
                values.append(value)
        lons = 0
        lats = 0
        lost_nodes = []
        for node_id in nodes:
            if node_id not in self.id_nodes2lat_lon:
                lost_nodes.append(node_id)
                continue
            lats += self.id_nodes2lat_lon[node_id][0]
            lons += self.id_nodes2lat_lon[node_id][1]
        if len(lost_nodes) > 0:
            print(lost_nodes)
        lats /= len(nodes)
        lons /= len(nodes)

        values[1] = lats
        values[2] = lons
        self.fill_row(keys, values, 'ways')

    def fill_row(self, keys: list, values: list, table: str):
        q = '?' + ', ?' * (len(values) - 1)
        keys = map(lambda x: f'[{x}]', keys)
        keys = '(' + ', '.join(keys) + ')'
        query = f"INSERT INTO {table} {keys} VALUES ({q})"
        self.cursor.execute(query, tuple(values))
