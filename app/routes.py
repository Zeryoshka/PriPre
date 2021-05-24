from app import app
from app import models
from app import DataManager
from flask import render_template, request

from plotly.utils import PlotlyJSONEncoder
import plotly.graph_objects as go

import json
import csv

def make_graph(ticket_list):
    fig = go.Figure()
    for ticket_data in ticket_list:
        fig.add_trace(ticket_data)
    layout = go.update_layout(
        title=go.layout.Title(text='PriPre ticket graph'),
        yaxis_title='Close value',
        xaxis_title='Date',
        legend_title='Tickets',
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="Black"
        )
    )

@app.route('/')
def index():
    # Заглушка, чтобы было проще понимать какие параметры требуются для рендера
    parametrs = {
        'tickets': DataManager.ticket_list, # Наимаенования тикетов (списком строк)
        'models': models.names # Наименования моделей (списком строк)
    }
    return render_template('index-template.html', **parametrs) # !Внимательнее там **parametrs


@app.route('/plot/past', methods=['GET', 'POST'])
def plot_past_view():
    # dict with to param ticket(str) and list of names's strings, named model
    params = request.get_json()

    # X, Y = get_data()
    # X, Y = receive_ml(X, Y)
    # plotly_graph = make_graph(X, Y)
    # return plotly_graph
    fig = go.Figure()
    return json.dumps(fig, cls=PlotlyJSONEncoder), 200, {'Content-Type': 'application/json'}
