import requests
from bs4 import BeautifulSoup
import re
import json
from pathlib import Path
import time
from concurrent.futures import ThreadPoolExecutor


def get_property_data_from_js(data, dict):
    """ Add """
    # get price
    dict["price"] = data["transaction"]["sale"]["price"]
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
                dict[l] = data["property"][prop][l]
        elif prop == "building":
            sub = ["constructionYear", "facadeCount", "floorCount"]
            for s in sub:
                if data["property"][prop] != None:
                    dict[s] = data["property"][prop][s]
                else:
                    dict[s] = None
        elif prop == "kitchen":
            if data["property"][prop] != None:
                dict[prop] = data["property"][prop]["type"]
            else:
                dict[prop] = None
        elif prop == "land":
            if data["property"][prop] != None:
                dict[prop] = data["property"][prop]["surface"]
            else:
                dict[prop] = None
        else:
            dict[prop] = data["property"][prop]
    # get energy consumption data
    if data["transaction"]["certificates"] != None:
        dict["primaryEnergyConsumptionPerSqm"] = data["transaction"]["certificates"]["primaryEnergyConsumptionPerSqm"]
        dict["epcScore"] = data["transaction"]["certificates"]["epcScore"]
    else:
        dict["primaryEnergyConsumptionPerSqm"] = None
        dict["epcScore"] = None
    if data["property"]["energy"] != None:
        dict["hasDoubleGlazing"] = data["property"]["energy"]["hasDoubleGlazing"]
    else:
        dict["hasDoubleGlazing"] = None
    # get sale type
    sale_type = None
    if data["flags"]["isPublicSale"]:
        sale_type = "PublicSale"
    elif data["flags"]["isNotarySale"]:
        sale_type = "NotarySale"
    elif data["flags"]["isLifeAnnuitySale"]:
        sale_type = "LifeAnnuitySale"
    elif data["flags"]["isAnInteractiveSale"]:
        sale_type = "AnInteractiveSale"
    dict["saleType"] = sale_type

    return dict


def scrape_property_data(id, session):
    """ Add """
    url = "https://www.immoweb.be/en/classified/" + id
    immo_data = {
        id: {}
    }
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
                immo_data[id] = get_property_data_from_js(js_data, immo_data[id])
                break
            else:
                continue
    return immo_data


def scrape_properties():
    """ Add """
    file_name = "properties_ids.txt"
    file_path = str(Path.cwd() / "data" / file_name)
    immo_data = {}
    with open(file_path, "r") as file:
        with requests.Session() as session:
            with ThreadPoolExecutor(max_workers=10) as executor:
                executor.map(lambda id: immo_data.update(scrape_property_data(id, session)), [id.strip() for id in file])
    return immo_data


def save_to_json(data):
    """ Add """
    file_name = "propreties_data.json"
    file_path = str(Path.cwd() / "data" / file_name)
    with open(file_path, "w", encoding="utf-8") as json_file:
        json_file.write(json.dumps(data, indent=4))


if __name__ == "__main__":
    start = time.time()
    save_to_json(scrape_properties())
    end = time.time()
    print("Time Taken: {:.6f}s".format(end-start))
