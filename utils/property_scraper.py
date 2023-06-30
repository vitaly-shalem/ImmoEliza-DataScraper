import requests
from bs4 import BeautifulSoup
import re
import json
from pathlib import Path
import time
from concurrent.futures import ThreadPoolExecutor


def get_js_data(data, dict):
    # get price
    dict["transactionType"] = data["transaction"]["type"]
    dict["transactionSubtype"] = data["transaction"]["subtype"]
    if data["transaction"]["sale"] != None:
        dict["price"] = data["transaction"]["sale"]["price"]
    elif data["transaction"]["rental"] != None:
        dict["price"] = data["transaction"]["rental"]["price"]
    else:
        dict["price"] = None
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
    elif data["flags"]["isInvestmentProject"]:
        sale_type = "InvestmentProject"
    elif data["flags"]["isNewRealEstateProject"]:
        sale_type = "NewRealEstateProject"
    #elif data["flags"]["isNewlyBuilt"]:
    #    sale_type = "NewlyBuilt"
    dict["saleType"] = sale_type
    # piblication date
    dict["creationDate"] = None
    dict["lastModificationDate"] = None
    if data["publication"] != None:
        dict["creationDate"] = data["publication"]["creationDate"]
        dict["lastModificationDate"] = data["publication"]["lastModificationDate"]

    return dict


def get_page_data(id, session):
    url = "https://www.immoweb.be/en/classified/" + id
    property_data = {
        id: {}
    }
    property_data[id]["URL"] = url

    req = session.get(url)
    status = req.status_code

    if status != 200:
        property_data[id]["Status"] = status
    else:
        property_data[id]["Status"] = status
        content = req.content
        s = BeautifulSoup(content, "html.parser")

        script_tags = s.find_all('script', {'type': 'text/javascript'})
        for st in script_tags:
            if st.text.find("window.classified") != -1:
                js_var = re.search(r"window\.classified = (\{.*\});", st.text)
                js_var_value = js_var.group(1)
                js_data = json.loads(js_var_value)
                property_data[id] = get_js_data(js_data, property_data[id])
                break
            else:
                continue
    return property_data


def scrape_from_txt():
    file_name = "properties_ids.txt"
    file_path = str(Path.cwd() / "data" / file_name)
    property_data = {}
    with open(file_path, "r") as file:
        with requests.Session() as session:
            with ThreadPoolExecutor(max_workers=10) as executor:
                executor.map(lambda id: property_data.update(get_page_data(id, session)), [id.strip() for id in file])
    return property_data


def save_to_json(data):
    file_name = "properties_data.json"
    file_path = str(Path.cwd() / "data" / file_name)
    with open(file_path, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)


def property_scraper():
    start = time.time()
    save_to_json(scrape_from_txt())
    end = time.time()
    print("Time taken to scrape listings: {:.6f}s".format(end-start))
