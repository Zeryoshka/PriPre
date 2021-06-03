import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
os.environ["CUDA_VISIBLE_DEVICES"]= '-1' 

from ml.it_is_alive import It_is_alive

import pandas as pd
from matplotlib import pyplot as plt
import requests
import apimoex

def form_data(security):
    '''
    for every ticket in security_list,
    gets data from moex, parses it to list of values
    and list of answers, writes it to {security}.csv
    '''
    with requests.Session() as session:
        data = apimoex.get_market_candles(
            session,
            security=security,
            start='2020-12-01',
            interval=10
        )
        df = pd.DataFrame(data)
        return df


df = form_data('SBER')[['begin', 'close']]
train = df[:5000]
train.index = range(train.shape[0])
test = df[5000:7000]
test.index = range(test.shape[0])

model = It_is_alive()
model.compile_model()
model.fit(train)
pred = model.lazy_predict(test)
train_pred = model.lazy_predict(train)

plt.plot(
    train['begin'], 
    train['close'], 
    color='red'
)
plt.plot(
    train_pred['begin'], 
    train_pred['close'],
    color='orange'
)
plt.plot(
    test['begin'],
    test['close'],
    color='blue'
)
plt.plot(
    pred['begin'], 
    pred['close'],
    color='green'
)
plt.show()