"""
This file contains DataManager class
Which are used in app package
"""

import os
import requests
import apimoex
import pandas as pd
from .config import START_DATE, END_DATE, SECURITY_LIST, DATA_PATH, INTERVAL


class DataManager:
    """
    Class to operate data
    _path_to_data : str, holds path to folder, there
    data is stored
    _ticket_list : list[str], holds list of current tickets in folder
    """

    @staticmethod
    def update_data(ticket_list=SECURITY_LIST, start_date=START_DATE, end_date=END_DATE, interval=INTERVAL, path=DATA_PATH) -> None:
        """
        Used for updating data as a class method
        Works same as get_data.py script
        """
        for security in ticket_list:
            with requests.Session() as session:
                data = apimoex.get_market_candles(
                    session,
                    security=security,
                    start=start_date,
                    interval=interval,
                    end=end_date,
                )
                whole_frame = pd.DataFrame(data)
                date, close = whole_frame["begin"], whole_frame["close"]
                attr = {"begin": date, "close": close}
                whole_frame = pd.DataFrame(attr)
                if not os.path.exists(path):
                    os.mkdir(path)
                whole_frame.to_csv(path + security + ".csv")

    def __init__(self, path=DATA_PATH) -> None:
        """
        Constructor for Data_manager object
        param: DATA_PATH - str
        """
        self._path_to_data = path
        self._ticket_list = list(map(lambda x: x.split(".")[0], os.listdir(DATA_PATH)))
        self.start_date = START_DATE
        self.end_date = END_DATE

    @property
    def ticket_list(self) -> list:
        """
        Gets list of strings
        Example -> ['YNDX', 'ALRS', 'SBER', 'MOEX']
        """
        return self._ticket_list

    def give_data(self, ticket: str, start_date=START_DATE, end_date=END_DATE) -> tuple:
        """
        Opens up csv file and reads it to two lists
        x_axis : list of datetime.datetime objects
        y_axis : list of float numbers
        """
        with open(self._path_to_data + ticket + ".csv", newline="") as csvfile:
            content = pd.read_csv(csvfile)
            values = content.loc[
                (content["begin"] >= start_date) & (content["begin"] <= end_date)
            ]
            x_axis, y_axis = values["begin"], values["close"]
            return x_axis, y_axis
