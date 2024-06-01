

from litestar import Litestar
from litestar import get


@get("/")
async def index() -> str:
    return "Hello, world!"


@get("/books/{book_id:int}")
async def get_book(book_id: int) -> dict[str, int]:
    return {"book_id": book_id}


import json
from litestar import post

@post("/parse")
async def parse(data: str) -> dict[str, str]:
    return json.loads(data)[0]

from dateutil import parser as date_parser

@post("/parse_du")
async def parse_du(data: str) -> dict[str, str]:
    val = json.loads(data)[0]["datetime"]
    res = date_parser.parse(val)
    return {"datetime": str(res)}


import datetime as dt

@post("/parse_iso")
async def parse_iso(data: str) -> dict[str, str]:
    val = json.loads(data)[0]["datetime"]
    res = dt.datetime.fromisoformat(val)
    return {"datetime": str(res)}


GLOBAL_VAR = []

@get("/leak")
async def leak() -> str:
    return GLOBAL_VAR.append(["Hello, world!"*len(GLOBAL_VAR)*10])


app = Litestar([index, get_book, parse, parse_du, parse_iso, leak])

import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=5000)

