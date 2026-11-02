import sqlite3
from datetime import datetime

from scraper import getPrice


def registerNewProduct():
    name = input("Enter the name of the product: ")
    url = input("Enter the url of the product: ")
    description = input("Enter a short description of the product: ")

    initialPrice = getPrice(url)

    if initialPrice == -1:
        print("Can't get the price of the product")
        return

    print(initialPrice)

    conexion = sqlite3.connect("productsHistory.db")
    cur = conexion.cursor()

    try:
        cur.execute(
            """
            INSERT OR IGNORE INTO product (name, url, description)
            VALUES (?, ?, ?)
        """,
            (name, url, description),
        )

        currentDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cur.execute(
            """
            INSERT INTO price (product, price, date) 
            VALUES (?, ?, ?)
        """,
            (name, initialPrice, currentDate),
        )

        conexion.commit()

        print("Product was stored successfully")

    except Exception as e:
        print(f"Couldn't save the product in the database: {e}")

    finally:
        conexion.close()


registerNewProduct()
