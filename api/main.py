from fastapi import FastAPI

urls = {
    "https://www.thomann.es/harley_benton_hbcg45.htm": {},
    "https://www.thomann.es/gibson_j_45_standard_vs_2026.htm": {},
}

app = FastAPI()


@app.get("/")
async def read_urls():
    return urls


@app.post("/products")
async def create_url(url: str):
    urls[url] = {}


@app.get("/products/{url}")
async def read_url(url: str):
    return urls[url]


@app.put("/products/{url}")
async def put_price({date, price}: dict):
    