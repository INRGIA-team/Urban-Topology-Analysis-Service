import re
import xml.etree.ElementTree as ET
from re import search
from dadata import Dadata
token = "c9bd181f9fd147bbb8259a3765caa38b5b61f942"
regex = r",( (ул|пр) ([\w\s-]+))|( ([\w\s-]+) (пр-д|пл)),"


def get_name(graph_root, id):
    dadata = Dadata(token)
    for node in graph_root.iter("node"):
        if node.get("id") == id:
            lat = node.get("lat")
            lon = node.get("lon")
            data = dadata.geolocate(name="address", lat=lat, lon=lon, count=1)[0].get('value')
            if data == None:
                return 'nan'
            match = re.search(regex, data)
            try:
                if match.group(2):
                    street_type = match.group(2)
                    if street_type == "ул":
                        street_name = match.group(3)+str(" улица")
                    else:
                        street_name = str("проезд ")+match.group(3)
                elif match.group(6):
                    street_type = match.group(6)
                    if street_type == "пл":
                        street_name = match.group(5)+str(" площадь")
                    else:
                        street_name = match.group(5)+str(" проезд")
                else:
                    street_name = 'nan'
                # print(street_name)
                return street_name
            except:
                # print(data)
                return 'nan'

            # index_start = data.find(" ул ")
            # index_end = data.find(",", index_start)
            # street_name = data[index_start + 1: index_end]
            # print(data)

    return 'nan'
