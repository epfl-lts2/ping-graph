import requests
import os
from lxml.html.soupparser import fromstring
import json
import io
import random


nodes = []
links = []
linked = []


if not os.path.isfile('pings.cache'):
    data = requests.get("https://wondernetwork.com/pings").text

    with open('pings.cache', 'wb') as f:
        f.write(data.encode('utf-8'))

with open('pings.cache', 'rb') as f:
    data = '\n'.join([x.decode('utf-8') for x in f.readlines()])

xml_data = fromstring(data)

m = 0

for a in xml_data.xpath("//td[contains(@class,'is-bucket')]/a"):

    __, __, city_from, city_to = a.attrib['href'].split('/')
    ping = a.text.strip()

    if ping[-2:] == "ms":
        ping = float(ping[:-2].replace(',', ''))

        if city_from not in nodes:
            nodes.append(city_from)

        if city_to not in nodes:
            nodes.append(city_to)

        m = max(ping, m)

        if (city_from, city_to) not in linked and (city_to, city_from) not in linked:
            if random.randint(0, 20) == 0 or ping < 100:
                links.append({'source': nodes.index(city_from), 'target': nodes.index(city_to), 'value': ping})
                linked.append((city_from, city_to))

nodes_mapping = {}
name = '?'
group_id = 0

with io.open('nodes.txt', 'r', encoding='utf-8') as f:
    for line in f.readlines():
        line = line.strip()

        if line:
            if line[0] == '#':
                name = line[1:]
                group_id += 1
            else:
                nodes_mapping[line] = {'group': group_id, 'group_name': name}

nodes = [{'name': x, 'group': nodes_mapping[x]['group'], 'group_name': nodes_mapping[x]['group_name']} for x in nodes]

final = {'nodes': nodes, 'links': links}

with io.open('data.json', 'w', encoding='utf-8') as f:
    json.dump(final, f)

print(len(links))
