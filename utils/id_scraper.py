import requests
from concurrent.futures import ThreadPoolExecutor
import time
import itertools
from pathlib import Path


def get_ids_from_page(page, property_types, session):
    ids = []
    for type in property_types:
        url_lists = "https://www.immoweb.be/en/search-results/%s/for-sale?countries=BE&page=%s&orderBy=newest" % (type, page)
        r = session.get(url_lists)
        ids += [listing['id'] for listing in r.json()["results"]]
    return ids


def get_ids(pages):
    with requests.Session() as session:
        with ThreadPoolExecutor(max_workers=30) as executor:
            result = list(executor.map(lambda page: get_ids_from_page(page, ['house', 'apartment'], session), range(1, pages+1)))
            flattened_result = list(itertools.chain.from_iterable(result))
            print(f"Number of ids: {len(flattened_result)}")
            return flattened_result


def save_to_txt(ids):
    file_name = "properties_ids.txt"
    file_path = Path.cwd() / "data" / file_name
    with open(file_path, 'w') as f:
        for id in ids:
            f.write('%s\n' % id)


def id_scraper(pages):
    start = time.time()
    ids = get_ids(pages)
    save_to_txt(ids)
    end = time.time()
    print("Time taken to scrape ids: {:.6f}s".format(end-start))
