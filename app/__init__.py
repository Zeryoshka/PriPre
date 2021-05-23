from flask import Flask

app = Flask(__name__)

from app.ml import models

from app import routes