"""
This file contains DataManager class
Which are used in app package
"""

import os
import pandas as pd
from .config import DATA_PATH, START_DATE, END_DATE


class DataManager:
    """
    Class to operate data
    _path_to_data : str, holds path to folder, there
    data is stored
    _ticket_list : list[str], holds list of current tickets in folder
    """

    def __init__(self):
        """
        Constructor for Data_manager object
        param: DATA_PATH - str
        """
        self._path_to_data = DATA_PATH
        self._ticket_list = list(
            map(lambda x: x.split(".")[0], os.listdir(DATA_PATH))
        )

    @property
    def ticket_list(self) -> list:
        """
        Gets list of strings
        Example -> ['YNDX', 'ALRS', 'SBER', 'MOEX']
        """
        return self._ticket_list

    def give_data(
        self, ticket, start_date=START_DATE, end_date=END_DATE
    ) -> tuple:
        """
        Opens up csv file and reads it to two lists
        x_axis : list of datetime.datetime objects
        y_axis : list of float numbers
        """
        with open(self._path_to_data + ticket + ".csv", newline="") as csvfile:
            content = pd.read_csv(csvfile)
            values = content.loc[
                (content["date"] >= start_date) & (content["date"] <= end_date)
            ]
            x_axis, y_axis = list(values["date"]), list(values["close_value"])
            return x_axis, y_axis
