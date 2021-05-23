from flask import Flask

app = Flask(__name__)

from app.ml import models

from data_manager import DataManager

from app import routes