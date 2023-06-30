from utils.id_scraper import id_scraper
from utils.property_scraper import property_scraper
from utils.json_to_csv import json_to_csv


def main():
    id_scraper(5)
    property_scraper()
    json_to_csv()


if __name__ == '__main__':
    main()
