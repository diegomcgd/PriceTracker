import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,"
        " like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "es-ES,es;q=0.9",
}

API_BASE_URL = "http://0.0.0.0:8000"


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


def get_all_products() -> dict | None:
    """Sends a request to the API to get the products"""

    products = requests.get(API_BASE_URL + "/products")

    if products.status_code != 200:
        return None

    return products.json()


# for each url, get today's price
# post url's price for today


def get_products_price(products: dict) -> bool:
    """Get today's price for each url and put it in the database"""

    for url in products:
        price = get_price(url)

        if price == -1:
            continue

        url_price = (str(url), price)

        request = requests.put(
            API_BASE_URL + "/products/history", params={"url": url_price}
        )

        if request.status_code != 200:
            return False

    return True


products = get_all_products()
print(products)

if products != None:
    get_products_price(products)
