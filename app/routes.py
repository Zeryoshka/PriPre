from app.app import app
from app.app import models
from app.app import data_manager

from flask import render_template
from flask import request

from plotly.utils import PlotlyJSONEncoder
import plotly.graph_objects as go

import json
import pandas as pd


@app.route("/")
def index():
    # Заглушка, чтобы было проще понимать какие параметры требуются для рендера
    parametrs = {
        # Наимаенования тикетов (списком строк)
        "tickets": data_manager.ticket_list,
        "models": models.names,  # Наименования моделей (списком строк)
    }
    # !Внимательнее там **parametrs
    return render_template("index-template.html", **parametrs)


@app.route("/plot/past", methods=["POST"])
def plot_past_view():
    # dict with to param ticket(str) and list of names's strings, named model
    params = request.get_json()
    ticket = params["ticket"]  # Ticket name from client
    model_list = params["models"]  # Models list : str

    X, Y = data_manager.give_data(ticket, start_date='2021-05-01', end_date='2021-06-01')
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=X, x0=X[0], y=Y, y0=Y[0], name="Real value"))
    fig.update_layout(
        title=go.layout.Title(text=f"PriPre {ticket} ticket graph"),
        yaxis_title="Close value",
        xaxis_title="Date",
        showlegend=True,
        legend_title_text="Tickets",
        font=dict(family="Courier New, monospace", size=18, color="Black"),
    )
    return (
        json.dumps(fig, cls=PlotlyJSONEncoder),
        200,
        {"Content-Type": "application/json"},
    )

@app.route("/stats/")
def display_stats():
    """
    Returns html page with stats selection
    """
    # dict with to param ticket(str) and list of names's strings, named model
    parametrs = {
        # Наимаенования тикетов (списком строк)
        "tickets": data_manager.ticket_list,
        "models": models.names,  # Наименования моделей (списком строк)
    }
    return render_template("stats-template.html", **parametrs)

# @app.route("stats/count", methods=["POST"])
# def count_stats():
#     params = request.get_json()
#     ticket = params["ticket"]  # Ticket name from client
#     period = params["start_date"] # Date to start count
#     pass