"""
This module interprets handling data
In config.py stored:
    - constants for selecting period,
    - path to data storage,
    - list of used tickets
DM.py contains Data_manager class, which used to:
    - return list of used tickets
    - get data for plotting
"""

from .data_manager import DataManager
from .config import PREDICTION_PATH

Data_Manager = DataManager()
