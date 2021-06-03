from flask import Flask
from data_manager import DataManager
from ml import Models
from ml import MODELS

app = Flask(__name__)
data_manager = DataManager()
models = Models(MODELS)
