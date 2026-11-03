import requests
from bs4 import BeautifulSoup
from datetime import datetime

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,"
        " like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "es-ES,es;q=0.9",
}

API_BASE_URL = "0.0.0.0:8000"


def get_price(url: str) -> float:

    content = requests.get(url, headers=headers)

    if content.status_code == 200:
        soup = BeautifulSoup(content.text, "html.parser")

        container = soup.find("div", class_="price fx-text fx-text--no-margin")

        if container:
            priceString = container.text.strip()

            price = float(
                priceString.replace("$", "")
                .replace("€", "")
                .replace(".", "")
                .replace(",", ".")
            )

            return price

        else:
            print("Price wasn't found")
            return -1

    else:
        print("There was an error with the get method")
        return -1


# get all urls
def get_all_urls() -> dict | None:
    urls = requests.get(API_BASE_URL + "/products")

    if urls.status_code != 200:
        return None

    return urls.json()


def get_prices(all_urls: dict):
    for url, prices in all_urls.items():
        price = get_price(url)
        prices[datetime.now()] = price


# for each url, get today's price
# post url's price for today
