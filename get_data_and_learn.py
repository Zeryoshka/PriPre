"""
This file implements script
Which loads data from apimoex
"""
from ml.it_is_alive.config import EPHOS_FIT
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
os.environ["CUDA_VISIBLE_DEVICES"]= '-1' 

from data_manager import DataManager
import data_manager
from ml import Models
import pandas as pd

PRICES_COUNT = 100
PATH = 'app/predict_data/'

def slice_data(df, train_len=5000):
    """
    Method for slice df
    """
    new_df = df.copy(deep=True)
    train = new_df.iloc[:train_len]
    train.index = range(train_len)
    test = new_df.iloc[train_len:]
    test.index = range(len(test))
    return train, test


if __name__ == "__main__":
    DataManager.update_data()
    print("""
        ---------------------------------
        Data updated
        ---------------------------------
    """)
    models = Models()
    data_manager = DataManager()
    for ticket in data_manager.ticket_list:
        dates, values = data_manager.give_data(ticket)
        data = pd.DataFrame({'begin' : dates.values, 'close' : values.values})
        train, test = slice_data(data)
        model = models['It is alive']
        print(model)
        model.compile_model()
        model.fit(train)
        print("---------------------------------")
        print(f"Learning finished with ticket {ticket}")
        print("---------------------------------")
        test_prediction = model.predict(train['close'][-PRICES_COUNT:], test['begin'])
        print("---------------------------------")
        print(f"Prediction finished with ticket {ticket}")
        print("---------------------------------")
        print(test_prediction)
        if not os.path.exists(PATH):
            os.mkdir(PATH)
        test_prediction.to_csv(PATH + ticket + ".csv")