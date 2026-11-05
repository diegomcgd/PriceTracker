from datetime import datetime
from uuid import uuid4

from fastapi import FastAPI, HTTPException

uuid_1 = str(uuid4())
uuid_2 = str(uuid4())

products: dict = {
    "https://www.thomann.es/harley_benton_hbcg45.htm": uuid_1,
    "https://www.thomann.es/gibson_j_45_standard_vs_2026.htm": uuid_2,
}

prices: dict = {
    uuid_1: {datetime.now().isoformat(): 100},
    uuid_2: {datetime.now().isoformat(): 2000},
}

app = FastAPI()


@app.get("/products")
async def read_products():
    """Get all the products in the database"""

    return products


@app.post("/products")
async def create_product(url: str):
    """Add a new product to the database"""

    uuid = str(uuid4())
    products[url] = uuid
    prices[uuid] = {}


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
