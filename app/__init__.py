from flask import Flask

app = Flask(__name__)

from data_manager import DataManager as data_manager
from app.ml import models
from app.routes import app
