"""
Contains flask view functions
Used to implement backend logic of app
"""

import json
import datetime
import pandas as pd

from plotly.utils import PlotlyJSONEncoder
import plotly.graph_objects as go

from flask import render_template
from flask import request
from flask import jsonify

from app.app import app
from app.app import models
from app.app import data_manager
from app.app import prediction_manager


def validate_data(date_text):
    """
    Function used for validating data
    In get_stats function
    Takes string with %Y-%m-%d data format
    """

    try:
        datetime.datetime.strptime(date_text, "%Y-%m-%d")
    except ValueError:
        return False
    return True


@app.route("/")
def index():
    """
    View which displays main page
    Parameters are
        - list of available tickets
        - list of available model names
    """

    parametrs = {
        "tickets": data_manager.ticket_list,
        "models": models.names,
    }

    return render_template("index-template.html", **parametrs)


@app.route("/plot/past", methods=["POST"])
def plot_past_view():
    """
    View which are used to make Plotly graph
    And sends it to client
    """

    params = request.get_json()
    ticket = params["ticket"]  # Ticket name from client
    model_list = params["models"]  # Models list : str

    dates, values = data_manager.give_data(ticket)
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=dates, y=values, name="Real value"
        )
    )
    if 'It is alive' in model_list:
        dates_pred, values_pred = prediction_manager.give_data(ticket)
        fig.add_trace(
        go.Scatter(
            x=dates_pred, y=values_pred, name="Predicted value"
        )
    )
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


@app.route("/stats/", methods=["GET"])
def display_stats():
    """
    Returns html page with stats selection
    Parameters are
        - list of available tickets
        - list of available model names
    """

    parametrs = {
        "tickets": data_manager.ticket_list,
        "min_date": data_manager.start_date,
        "max_date": data_manager.end_date
    }

    return render_template("stats.html", **parametrs)


@app.route("/get_stats", methods=["GET"])
def count_stats():
    """
    View which sends to client
    JSON with needed values of given ticket and period
    """

    ticket = request.args["ticket"]
    if ticket not in data_manager.ticket_list:
        return 400
    period_start, period_end = (
        request.args["date_start"],
        request.args["date_end"],
    )
    if not (validate_data(period_start) and validate_data(period_end)):
        return 400
    dates, values = data_manager.give_data(
        ticket=ticket, start_date=period_start, end_date=period_end
    )
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=list(dates), y=list(values), name="Real value"
        )
    )
    fig.update_layout(
        title=go.layout.Title(text=f"PriPre {ticket} ticket graph"),
        yaxis_title="Close value",
        xaxis_title="Date",
        showlegend=True,
        legend_title_text="Tickets",
        font=dict(family="Courier New, monospace", size=18, color="Black"),
    )
    values = pd.Series(data=values.values, index=dates)
    answer = {
        "chart": fig.to_dict(),
        "stats": {
            "std": values.std(),
            "avg": values.mean(),
            "median": values.median(),
            "mode": values.mode()[0],
            "variants": values.var()
        }
    }
    return json.dumps(answer)
