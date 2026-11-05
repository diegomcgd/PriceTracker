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
    """Get the price of a product given its url"""

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


def put_new_prices(products: dict) -> bool:
    """Put the new price of every product in the database"""

    for url, uuid in products.items():
        price = get_price(url)

        if price == -1:
            continue

        request = requests.put(
            # There are three ways to send parameters to the API:
            #   - In the path, just adding it to the url
            #   - As querys (?price=3000). In requests, we have to add into params a dictionary with the pair {"name_of_the_param": value_of_the_param}
            #   - In the body of the request
            # In this case, I'm sending the price as a query, creating a dictionary with the name of the variable and its value
            API_BASE_URL + "/products/" + uuid + "/prices",
            params={"price": price},
        )

        if request.status_code != 200:
            print("Price wasn't put in the database. Url: " + url)
            return False

    return True


def main():
    products = get_all_products()
    if products != None:
        put_new_prices(products)


main()
