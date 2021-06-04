"""
Contains flask view functions
Used to implement backend logic of app
"""

import json
import pandas as pd

from plotly.utils import PlotlyJSONEncoder
import plotly.graph_objects as go

from flask import render_template
from flask import request

from app.app import app
from app.app import models
from app.app import data_manager


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

    dates, values = data_manager.give_data(
        ticket, start_date="2021-05-01", end_date="2021-06-03"
    )
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, x0=dates[0], y=values, y0=values[0], name="Real value"))
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
    Parameters are
        - list of available tickets
        - list of available model names
    """

    parametrs = {
        "tickets": data_manager.ticket_list,
        "models": models.names,
    }

    return render_template("stats-template.html", **parametrs)


@app.route("/stats/count", methods=["GET"])
def count_stats():
    """
    View which sends to client
    JSON with needed values of given ticket and period
    """
    # params = request.get_json()
    ticket = "YNDX"  # params["ticket"] Ticket name from client
    period_start, period_end = (
        "2021-01-01",
        "2021-04-04",
    )  # params["start_date"], params["end_date"]  Date to start count
    dates, values = data_manager.give_data(
        ticket=ticket, start_date=period_start, end_date=period_end
    )
    values = pd.Series(data=values, index=dates)
    answer = {
        "standard_square": values.std(),
        "mean_value": values.mean(),
        "median_value": values.median(),
        "mode_value": values.mode()[0],
        "variance": values.var(),
    }

    return json.dumps(answer)
