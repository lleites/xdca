import calendar
from dataclasses import dataclass
from typing import Dict

import pandas as pd
import pandas_datareader.data as web

DATA_SOURCE = "yahoo"


@dataclass
class Stats:
    min_avg_freq: Dict[str, int]
    start_date: str
    end_date: str


def get_history(ticker: str, start: str, end: str) -> pd.DataFrame:
    print("Downloading data...")  # noqa: T201

    history = web.DataReader(ticker, DATA_SOURCE, start=start, end=end)

    history = history[["High", "Low"]]

    return history


def enrich_data(data: pd.DataFrame) -> pd.DataFrame:
    print("Enriching data...")  # noqa: T201

    data["week_day"] = data.index.weekday

    data["avg"] = (data["High"] + data["Low"]) / 2

    data["week_key"] = data.index.year + data.index.isocalendar().week

    return data


def calculate_stats(
    history: pd.DataFrame, start_date: str, end_date: str
) -> Stats:
    print("Calculating stats ...")  # noqa: T201

    min_per_week_key = history.sort_values(
        ["week_key", "avg"], ascending=False
    ).drop_duplicates(subset="week_key")

    grouped_by_week_day = min_per_week_key.groupby("week_day").aggregate(
        {"avg": "count"}
    )

    grouped_by_week_day = grouped_by_week_day.rename(
        columns={"avg": "min_avg_freq"}
    )
    grouped_by_week_day.index = grouped_by_week_day.index.map(
        calendar.day_name.__getitem__
    )

    return Stats(
        start_date=start_date,
        end_date=end_date,
        **grouped_by_week_day.to_dict(),
    )


def main(ticker: str, start_date: str, end_date: str) -> Stats:

    history = get_history(ticker, start_date, end_date)

    enriched_data = enrich_data(history)

    stats = calculate_stats(enriched_data, start_date, end_date)

    return stats


if __name__ == "__main__":

    stats = main(ticker="MSFT", start_date="2020-09-10", end_date="2021-09-10")

    print(f"Stats: {stats=}")  # noqa: T201
