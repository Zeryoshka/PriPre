"""
This file implements script
Which loads data from apimoex
"""
import os
import pandas as pd

from ml import Models

from data_manager import DataManager
from data_manager import LAZY_PREDICTION_PATH


PRICES_COUNT = 100
PATH = 'app/predict_data/'

def slice_data(data_f, train_len=50000):
    """
    Method for slice df
    """
    new_data_f = data_f.copy(deep=True)
    train_data = new_data_f.iloc[:train_len]
    train_data.index = range(train_len)
    test_data = new_data_f.iloc[train_len:]
    test_data.index = range(len(test_data))
    return train_data, test_data


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
        if not os.path.exists(PATH):
            os.mkdir(PATH)
        test_prediction.to_csv(PATH + ticket + ".csv")
        print("---------------------------------")
        print(f"Prediction finished with ticket {ticket}")
        print("---------------------------------")
        test_prediction = model.lazy_predict(test)
        if not os.path.exists(LAZY_PREDICTION_PATH):
            os.mkdir(LAZY_PREDICTION_PATH)
        test_prediction.to_csv(LAZY_PREDICTION_PATH + ticket + ".csv")
        print("---------------------------------")
        print(f"Lazy prediction finished with ticket {ticket}")
        print("---------------------------------")
