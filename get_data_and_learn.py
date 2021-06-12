"""
This file implements script
Which loads data from apimoex
"""

from data_manager import DataManager, Data_Manager
import data_manager
from ml import Models

PRICES_COUNT = 100

def slice_data(df, train_len=5000):
    """
    Method for slice df
    """
    new_df = df.iloc.copy(deep=True)
    train = new_df.iloc[:train_len]
    train.index = range(train_len)
    test = new_df.iloc[train_len:]
    test.index = len(test)
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
        train, test = slice_data(data_manager.give_data(ticket))
        for model in models:
            model.compile_model()
            model.fit(train)
            print("""
                ---------------------------------
                Learning finished
                ---------------------------------
            """)
            test_prediction = model.predict(train['close'][-PRICES_COUNT:], test['close'])
            print("""
                ---------------------------------
                Prediction finished
                ---------------------------------
            """)
            #Дописать сохранение