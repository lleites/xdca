import pytest
from xdca import Stats, __version__, main


def test_version():
    assert __version__ == "0.1.0"


@pytest.mark.vcr()
def test_main():
    expected_stats = Stats(
        min_avg_freq={"Monday": 10, "Tuesday": 14, "Wednesday": 5, "Thursday": 7, "Friday": 16},
        start_date="2020-09-10",
        end_date="2021-09-10",
    )
    assert main(ticker="MSFT", start_date="2020-09-10", end_date="2021-09-10") == expected_stats
