import xml.etree.ElementTree as ET
import requests
from urllib.request import urlopen
import os
import sqlite3

default_url = "http://overpass-api.de/api/interpreter"
# query = 'node["name"="Екатеринбург"];' \
#         'out body;'
# query = query.encode("utf-8")

# response = requests.get('https://overpass-api.de/api/map?bbox=60.17212,56.65019,61.03455,56.96295')
#
#
# with open('/Users/yanakosareva/PycharmProjects/pythonProject1/ekb.xml',
#           'wb') as f:
#     for chunk in response.iter_content(chunk_size=10 * 1024 * 1024):
#         if chunk:
#             f.write(chunk)
b = '1'

# СОЗДАНИЕ БД

db = sqlite3.connect('ekb.db')
cursor = db.cursor()

# ПАРСЕР

tree = ET.iterparse('/Users/yanakosareva/PycharmProjects/pythonProject1/map')
rows_count = 0
node_tags = set()
way_tags = set()


def do():
    global rows_count
    for event, elem in tree:
        rows_count += 1
        if elem.tag == 'node':
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
        # elif elem.tag == 'relation':


# ФОРМИРОВАНИЕ СТОЛБЦОВ В ТАБЛИЦАХ
# ПОГУГЛИТЬ ПРО КВАДРАТНЫЕ СКОПКИ ВОЗЛЕ tag
node_fields = ''
for tag in node_tags:
    node_fields += f', [{tag}] TEXT'
way_fields = ''
for tag in way_tags:
    way_fields += f', [{tag}] TEXT'

cursor.execute(f"CREATE TABLE IF NOT EXISTS nodes "
               f"(id INTEGER,"
               f"lat DOUBLE,"
               f"lon DOUBLE"
               f"{node_fields})")
cursor.execute(f"CREATE TABLE IF NOT EXISTS ways "
               f"(id INTEGER,"
               f"nodes TEXT"
               f"{way_fields})")


# ЗАПОЛНЕНИЕ БАЗЫ


def parse_node(elem):
    tags = list(elem)
    attributes = elem.attrib
    keys = ['id', 'lat', 'lon']
    values = [attributes['id'], attributes['lat'], attributes['lon']]
    for tag in tags:
        key = tag.attrib['k'].lower()
        value = tag.attrib['v']
        keys.append(key)
        values.append(value)


def fill_row(keys, values):
    global cursor
    cursor.execute()


del tree
db.commit()
