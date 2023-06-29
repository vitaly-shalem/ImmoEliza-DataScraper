import requests
from concurrent.futures import ThreadPoolExecutor
import time
import itertools
from pathlib import Path


def get_ids_from_page(page, session, property_type):
    ids = []
    url_lists = "https://www.immoweb.be/en/search-results/%s/for-sale?countries=BE&page=%s&orderBy=newest" % (property_type, page)
    r = session.get(url_lists)
    ids = [listing['id'] for listing in r.json()["results"]]
    return ids


def get_ids(pages, property_type):
    with requests.Session() as session:
        with ThreadPoolExecutor(max_workers=30) as executor:
            result = list(executor.map(lambda page: get_ids_from_page(page, session, property_type), range(1, pages+1)))
            flattened_result = list(itertools.chain.from_iterable(result))
            print(f"Number of ids: {len(flattened_result)}")
            return flattened_result


def save_to_txt(ids, property_type):
    file_name = Path(f"{property_type}_listing_ids.txt")
    file_path = Path.cwd() / "data" / file_name
    with open(file_path, 'w') as f:
        for id in ids:
            f.write('%s\n' % id)


def id_scraper(pages, property_type):
    """
    Scrape ids and save them into a text file.

    @param pages: number of pages to scrape.
    @param property_type: type of property to scrape.
    """
    if property_type == "house" or property_type == "apartment":
        start = time.time()
        ids = get_ids(pages, property_type)
        save_to_txt(ids, property_type)
        end = time.time()
        print("Time taken to scrape ids: {:.6f}s".format(end-start))
    else:
        print(
            "Invalid argument: please use 'house' or 'apartment' as second argument.")
        return


if __name__ == "__main__":
    id_scraper(10, "apartment")
