import requests
import apimoex
import pandas as pd
from config import START_DATE, SECURITY_LIST, DATA_PATH

def form_data() -> None:
    """
    for every ticket in security_list,
    gets data from moex, parses it to list of values
    and list of answers, writes it to {security}.csv
    """
    for security in SECURITY_LIST:
        with requests.Session() as session:
            data = apimoex.get_market_candles(session, security=security, start=START_DATE)
            df = pd.DataFrame(data)
            date, close = list(map(lambda x: x.split()[0], \
                df['begin'].values)), df['close']
            attr = {'date' : date, 'close_value' : close}
            df = pd.DataFrame(attr)
            df.to_csv(DATA_PATH + security + '.csv')

if __name__ == '__main__':
    form_data()
