from app import app
from flask import render_template
import requests
import apimoex
import pandas as pd
import matplotlib.pyplot as plt


@app.route('/')
def index():
    return render_template('base.html')

@app.route('/info/<ticket>')
def info(ticket):
    with requests.Session() as session:
        data = apimoex.get_market_candles(session, ticket, interval = 24, start = '2021-04-01', end = '2021-05-05')
        df = pd.DataFrame(data)
        return render_template('info.html', df=df.items())
