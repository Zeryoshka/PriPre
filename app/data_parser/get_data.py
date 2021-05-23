import requests
import apimoex
import pandas as pd
# from config import START_DATE, SECURITY_LIST, DATA_PATH

def form_data() -> None:
    """
    for every ticket in security_list,
    gets data from moex, parses it to list of values
    and list of answers, writes it to {security}.csv
    """
    security_list = ['YNDX', 'ALRS', 'SBER', 'MOEX']
    for security in security_list:
        with requests.Session() as session:
            data = apimoex.get_market_candles(session, security=security, start='2021-01-01')
            df = pd.DataFrame(data)
            date, close, value = list(map(lambda x: x.split()[0], \
                df['begin'].values)), df['close'], df['value']
            attr = {'date' : date, 'close_value' : close, 'values' : value}
            df = pd.DataFrame(attr)
            df.to_csv('app/data_parser/loaded_data/' + security + '.csv')

if __name__ == '__main__':
    form_data()
