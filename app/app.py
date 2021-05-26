from flask import Flask
from data_manager import Data_manager
from ml import Models
from ml import MODELS

app = Flask(__name__)
data_manager = Data_manager()
models = Models(MODELS)
