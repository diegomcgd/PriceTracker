from api import main as api
from scraper import scraper


def main():
    products = api.read_urls()

    print(products)


main()
