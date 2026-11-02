import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,"
        " like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "es-ES,es;q=0.9",
}


def getPrice(url: str) -> str:

    content = requests.get(url, headers=headers)

    if content.status_code == 200:
        soup = BeautifulSoup(content.text, "html.parser")

        container = soup.find("div", class_="price fx-text fx-text--no-margin")

        if container:
            price = container.text.strip()
            return price

        else:
            print("Price wasn't found")
            return ""

    else:
        print("There was an error with the get method")
        return ""
