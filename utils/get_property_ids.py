import requests
from concurrent.futures import ThreadPoolExecutor
import time
import itertools


def get_ids_from_page(page, session):
    ids = []
    url_lists = f"https://www.immoweb.be/en/search-results/house-and-apartment/for-sale?countries=BE&page={page}&orderBy=newest"
    r = session.get(url_lists)
    ids = [listing['id'] for listing in r.json()["results"]]
    return ids


def get_ids(pages, max_workers):
    with requests.Session() as session:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            start = time.time()
            result = list(executor.map(lambda page: get_ids_from_page(page, session), range(1, pages+1)))
            flattened_result = list(itertools.chain.from_iterable(result))
            end = time.time()
            print(f"Number of ids: {len(flattened_result)}")
            print("Time Taken: {:.6f}s".format(end-start))
            return flattened_result
