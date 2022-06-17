from datetime import date, timedelta

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles

from xdca import Stats, main

app = FastAPI()


@app.get("/stats/{ticker}")
def stats(ticker: str) -> Stats:
    today = date.today()
    one_year_ago = today - timedelta(days=365)
    stats = main(
        ticker, start_date=one_year_ago.isoformat(), end_date=today.isoformat()
    )

    if not stats:
        raise HTTPException(
            status_code=404,
            detail="Ticker not found",
        )
    else:
        return stats


app.mount("/", StaticFiles(directory="pyscript", html=True), name="static")
