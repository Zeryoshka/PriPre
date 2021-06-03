"""
This file implements script
Which loads data from apimoex
"""
import os
import requests
import apimoex
import pandas as pd
from .config import START_DATE, END_DATE, SECURITY_LIST, DATA_PATH, INTERVAL


def form_data() -> None:
    """
    for every ticket in security_list,
    gets data from moex, parses it to list of values
    and list of answers, writes it to {security}.csv
    """
    for security in SECURITY_LIST:
        with requests.Session() as session:
            data = apimoex.get_market_candles(
                session,
                security=security,
                start=START_DATE,
                interval=INTERVAL,
                end=END_DATE,
            )
            whole_frame = pd.DataFrame(data)
            date, close = whole_frame["begin"], whole_frame["close"]
            attr = {"date": date, "close_value": close}
            whole_frame = pd.DataFrame(attr)
            if not os.path.exists(DATA_PATH):
                os.mkdir(DATA_PATH)
            whole_frame.to_csv(DATA_PATH + security + ".csv")


if __name__ == "__main__":
    form_data()
