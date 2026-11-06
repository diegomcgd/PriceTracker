import json
from datetime import datetime
from uuid import uuid4

from fastapi import FastAPI, HTTPException

# With FastAPI, the serialization is made by the framework automatically
# Serialize: transforms a python object to Json file
# Deserialize: transforms a Json file in a python object

uuid_1 = str(uuid4())
uuid_2 = str(uuid4())


prices: dict = {
    uuid_1: {datetime.now().isoformat(): 100},
    uuid_2: {datetime.now().isoformat(): 2000},
}

app = FastAPI()


@app.get("/products")
def read_products():
    """Get all the products in the database"""

    with open("api/products.json", mode="r", encoding="UTF_8") as file:
        products = json.load(file)
        products_ret = products["products"]
        return products_ret


@app.post("/products")
def create_product(url: str):
    """Add a new product to the database"""

    with open("api/products.json", mode="r+", encoding="UTF_8") as file:
        products = json.load(file)
        uuid = str(uuid4())
        products["products"][url] = uuid
        file.seek(0)
        file.truncate()
        json.dump(products, file)


@app.get("/products/{uuid}/prices")
async def read_prices(uuid: str) -> dict | None:
    """Get the prices history of a product"""

    if uuid not in prices:
        raise HTTPException(status_code=404, detail="There is no product with that id")
    return prices[uuid]


@app.put("/products/{uuid}/prices")
async def put_price(uuid: str, price: float):
    """Add a new price into a product"""

    if uuid not in prices:
        raise HTTPException(status_code=404, detail="There is no product with that id")
    prices[uuid][datetime.now().isoformat()] = price


def prueba(uuid: str):
    """Get the prices history of a product"""

    with open("api/prices.json", mode="r", encoding="UTF_8") as file:
        prices = json.load(file)
        print(prices[prices])


prueba("e9cff370-8148-4047-8460-546060fe4b57")
