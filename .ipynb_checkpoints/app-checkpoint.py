import datetime as dt
import json

from litestar import Litestar, get, post
import uvicorn

try:
    from dateutil import parser as date_parser
except ImportError:
    pass


GLOBAL_VAR = []


@get("/")
async def index() -> str:
    return "Hello, world!"


@get("/books/{book_id:int}")
async def get_book(book_id: int) -> dict[str, int]:
    return {"book_id": book_id}


@post("/parse")
async def parse(data: str) -> dict[str, str]:
    return json.loads(data)[0]


@post("/parse_du")
async def parse_du(data: str) -> str:
    val = json.loads(data)[0]['datetime']
    res = date_parser.parse(val)
    return str(res)


@post("/parse_iso")
async def parse_iso(data: str) -> str:
    val = json.loads(data)[0]['datetime']
    res = dt.datetime.fromisoformat(val)
    return str(res)


@get("/leak")
async def leak() -> str:
    return GLOBAL_VAR.append(["Hello, world!"*len(GLOBAL_VAR)*10])


app = Litestar([index, get_book, parse, parse_du, parse_iso, leak])

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=5000)

