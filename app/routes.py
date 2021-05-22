from app import app
from flask import render_template, request
# from config import SECURITY_LIST
import plotly.graph_objects as go
import csv

SECURITY_LIST = ['YNDX', 'ALRS', 'SBER', 'MOEX']
CSV_PATH = 'data_parser'

def parse_json(json):
    pass

def get_data(SECURITY_LIST, CSV_PATH):
    data = dict()
    for security in SECURITY_LIST:
        X = []
        Y = []
        with open(CSV_PATH + security +'.csv', newline='') as csvfile:
            content = csv.DictReader(csvfile)
            line_count = 0
            for row in line_count:
                if line_count:
                    X.append(row['date'])
                    Y.append(row['close_value'])
                line_count += 1
        data[security] = (X, Y)
    return data

def receive_ml(X, Y):
    pass

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
        'tickets': ['YNDX', 'ALRS', 'SBER', 'MOEX'], # Наимаенования тикетов (списком строк)
        'models': ['model 1', 'model 2', 'model 3'] # Наименования моделей (списком строк)
    }
    return render_template('index-template.html', **parametrs) # !Внимательнее там **parametrs
    # return render_template('index.html')

@app.route('/plot/past', methods=['GET', 'POST'])
def plot_past_view(ticket):
    params = parse_json(request.json)
    X, Y = get_data(params)
    X, Y = receive_ml(X, Y)
    plotly_graph = make_graph(X, Y)
    return plotly_graph
