from app import app
from app import models
from app import DataManager
from flask import render_template, request

from plotly.utils import PlotlyJSONEncoder
import plotly.graph_objects as go

import json

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
    ticket = params['ticket']
    X, Y = DataManager.give_data(ticket)
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=X,
            x0=X[0],
            y=Y,
            y0=Y[0],
            name='Real value'
        )
    )
    fig.update_layout(
        title=go.layout.Title(text=f'PriPre {ticket} ticket graph'),
        yaxis_title='Close value',
        xaxis_title='Date',
        showlegend=True,
        legend_title_text='Tickets',
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="Black"
        
        )
    )
    return json.dumps(fig, cls=PlotlyJSONEncoder), 200, {'Content-Type': 'application/json'}
