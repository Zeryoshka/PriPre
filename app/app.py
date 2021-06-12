"""
File to include all needed imports
"""

from flask import Flask
from data_manager import DataManager
# from ml import Models
# from ml import MODELS

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