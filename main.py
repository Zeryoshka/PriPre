import requests
import apimoex
import pandas as pd


with requests.Session() as session:
    data = apimoex.get_market_candles(session, 'SBER', interval = 24, start = '202', end = '2021-02-26')
    df = pd.DataFrame(data)
    print(df.head(), '\n')
    print(df.tail(), '\n')
    df.info()
    for part in data:
        print(part)
