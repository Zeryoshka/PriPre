from flask import Flask

app = Flask(__name__)

from data_manager import DataManager
from app.ml import models
from app import routes