import requests
from bs4 import BeautifulSoup
import re
import json


def get_property_data_from_js(id, data):
    """ Add """
    # get price
    immo_data[id]["price"] = data["transaction"]["sale"]["price"]
    # get property data
    property = ["type", "subtype", "location",
                "bedroomCount", "netHabitableSurface", "building", "hasLift", "kitchen",
                "hasGarden", "gardenSurface", "hasTerrace", "terraceSurface", "land",
                "fireplaceExists", "hasSwimmingPool", "hasAirConditioning",
                "bathroomCount", "showerRoomCount", "toiletCount",
                "parkingCountIndoor", "parkingCountOutdoor", "parkingCountClosedBox"]
    for prop in property:
        if prop == "location":
            loc = ["country", "region", "province", "district", "locality", 
                   "postalCode", "street", "number", "box", "floor"]
            for l in loc:
                immo_data[id][l] = data["property"][prop][l]
        elif prop == "building":
            sub = ["constructionYear", "facadeCount", "floorCount"]
            for s in sub:
                if data["property"][prop] != None:
                    immo_data[id][s] = data["property"][prop][s]
                else:
                    immo_data[id][s] = None
        elif prop == "kitchen":
            if data["property"][prop] != None:
                immo_data[id][prop] = data["property"][prop]["type"]
            else:
                immo_data[id][prop] = None
        elif prop == "land":
            if data["property"][prop] != None:
                immo_data[id][prop] = data["property"][prop]["surface"]
            else:
                immo_data[id][prop] = None
        else:
            immo_data[id][prop] = data["property"][prop]
    # get energy consumption data
    if data["transaction"]["certificates"] != None:
        immo_data[id]["primaryEnergyConsumptionPerSqm"] = data["transaction"]["certificates"]["primaryEnergyConsumptionPerSqm"]
        immo_data[id]["epcScore"] = data["transaction"]["certificates"]["epcScore"]
    else:
        immo_data[id]["primaryEnergyConsumptionPerSqm"] = None
        immo_data[id]["epcScore"] = None
    if data["property"]["energy"] != None:
        immo_data[id]["hasDoubleGlazing"] = data["property"]["energy"]["hasDoubleGlazing"]
    else:
        immo_data[id]["hasDoubleGlazing"] = None
    sale_type = None
    if data["flags"]["isPublicSale"]:
        sale_type = "PublicSale"
    elif data["flags"]["isNotarySale"]:
        sale_type = "NotarySale"
    elif data["flags"]["isLifeAnnuitySale"]:
        sale_type = "LifeAnnuitySale"
    elif data["flags"]["isAnInteractiveSale"]:
        sale_type = "AnInteractiveSale"
    immo_data[id]["saleType"] = sale_type
    


def scrape_property_data(id, session):
    """ Add """
    url = "https://www.immoweb.be/en/classified/" + id
    immo_data[id] = dict()
    immo_data[id]["URL"] = url
    
    req = session.get(url)
    status = req.status_code

    if status != 200:
        immo_data[id]["Status"] = status
    else:
        immo_data[id]["Status"] = status
        content = req.content
        s = BeautifulSoup(content, "html.parser")
            
        script_tags = s.find_all('script', {'type': 'text/javascript'})
        for st in script_tags:
            if st.text.find("window.classified") != -1:
                js_var = re.search(r"window\.classified = (\{.*\});", st.text)
                js_var_value = js_var.group(1)
                js_data = json.loads(js_var_value)
                #immo_data[id]["Data"] = js_data
                get_property_data_from_js(id, js_data)
                break
            else:
                continue

immo_data = dict()

def scrape_properties(file):
    """ Add """
    file = open(file + ".txt", "r")
    count = 0
    session = requests.Session()
    for line in file.readlines():
        id = line.strip()
        # Add concurrency
        # Send scrape_property_data to multiple workers
        if id not in immo_data.keys():
            scrape_property_data(id, session)
        count += 1
        if count % 10 == 0:
            print(count)


def save_to_json(file):
    """ Add """
    output = file + "_data.json"
    with open(output, "w", encoding="utf-8") as json_file:
        json_file.write(json.dumps(immo_data, indent=4))
    return output
