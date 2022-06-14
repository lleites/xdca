from datetime import date, timedelta

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from xdca import Stats, main

app = FastAPI()


@app.get("/stats/{ticker}")
def stats(ticker: str) -> Stats:
    today = date.today()
    one_year_ago = today - timedelta(days=365)
    return main(ticker, start_date=one_year_ago.isoformat(), end_date=today.isoformat())


app.mount("/", StaticFiles(directory="pyscript"), name="static")
