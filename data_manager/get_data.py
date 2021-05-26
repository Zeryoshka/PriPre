from genericpath import exists
import requests
import apimoex
import pandas as pd
from config import START_DATE, SECURITY_LIST, DATA_PATH, INTERVAL
import os


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
                interval=INTERVAL)
            df = pd.DataFrame(data)
            date, close = df['begin'], df['close']
            attr = {'date': date, 'close_value': close}
            df = pd.DataFrame(attr)
            if not os.path.exists(DATA_PATH):
                os.mkdir(DATA_PATH)
            df.to_csv(DATA_PATH + security + '.csv')


if __name__ == '__main__':
    form_data()
