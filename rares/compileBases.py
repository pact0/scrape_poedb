import json
from json.decoder import JSONDecoder
from RePoE import base_items

import time


baseGroups = json.load(open('./rareBaseIcons.json'))

CoEBases = json.load(open('./CoEBases.json'))

def getBases():
    result = {}
    for base,baseAttribs in baseGroups.items():
        CoEBase = {}
        RePoEBase = {}


        for item in CoEBases:
            if item["name_bitem"] == base:
                CoEBase = item

        for attribs in base_items.values():
            if attribs["name"] == base:
                RePoEBase = attribs


        resItem = {
            'base': base,
            'baseGroup': "",
            'id_bitem': "",
            'id_base': "",
            'drop_level': 0,
            'icon': baseAttribs["icon"],
            'w': 0,
            'h': 0,
            'old_image': "",
            'is_legacy': "0",
            'requirements': {},
            'properties': {},
            'implicits': [],
            'tags': []
        }

        print(base, RePoEBase["item_class"])
        resItem["baseGroup"] = RePoEBase["item_class"]
        resItem["id_bitem"] = CoEBase["id_bitem"]
        resItem["id_base"] = CoEBase["id_base"]
        resItem["drop_level"] = CoEBase["drop_level"]
        resItem["w"] = RePoEBase["inventory_width"]
        resItem["h"] = RePoEBase["inventory_height"]
        resItem["old_image"] = RePoEBase["visual_identity"]["dds_file"]
        resItem["is_legacy"] = CoEBase["is_legacy"]
        resItem["requirements"] = RePoEBase["requirements"]
        resItem["properties"] = CoEBase["properties"]
        resItem["implicits"] = CoEBase["implicits"]
        resItem["tags"] = RePoEBase["tags"]

        result.update({"{}".format(base): resItem})

    return result


with open("result.json", "w") as write_file:
    json.dump(getBases(), write_file)
