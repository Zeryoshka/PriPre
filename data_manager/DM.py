import csv
from datetime import datetime
import os
from .config import DATA_PATH


class Data_manager:
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
        self._ticket_list = list(map(lambda x: x.split(".")[0], os.listdir(DATA_PATH)))

    @property
    def ticket_list(self) -> list:
        """
        Gets list of strings
        Example -> ['YNDX', 'ALRS', 'SBER', 'MOEX']
        """
        return self._ticket_list

    def give_data(self, ticket) -> tuple:
        """
        Opens up csv file and reads it to two lists
        X : list of datetime.datetime objects
        Y : list of float numbers
        """
        X = []
        Y = []
        with open(self._path_to_data + ticket + ".csv", newline="") as csvfile:
            content = csv.DictReader(csvfile)
            line_count = 0
            for row in content:
                if line_count:
                    X.append(datetime.strptime(row["date"], "%Y-%m-%d %H:%M:%S"))
                    Y.append(float(row["close_value"]))
                line_count += 1
        return X, Y
