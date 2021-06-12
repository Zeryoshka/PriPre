"""
File to include all needed imports
"""

from flask import Flask
from data_manager import DataManager
from data_manager import PREDICTION_PATH

class Models():
    """
    cover
    """
    def __init__(self):
        """
        cover
        """
        self.names =  ["It is alive"]

models = Models()

app = Flask(__name__)
data_manager = DataManager()
prediction_manager = DataManager(PREDICTION_PATH)