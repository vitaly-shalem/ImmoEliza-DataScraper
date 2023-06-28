import requests
import time

url_lists = "https://www.immoweb.be/en/search-results/house-and-apartment/for-sale?countries=BE&page=1&orderBy=newest"


def get_ids(pages, session):
    ids = []
    for page in range(pages):
        url_lists = f"https://www.immoweb.be/en/search-results/house-and-apartment/for-sale?countries=BE&page={page}&orderBy=newest"
        r = session.get(url_lists)
        ids += [listing['id'] for listing in r.json()["results"]]
    return ids


with requests.Session() as session:

    start = time.time()
    ids = get_ids(20, session)
    end = time.time()
    print(f"retrieved {len(ids)} ids in {end - start} seconds")
