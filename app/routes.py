from app import app
from flask import render_template, request
import matplotlib.pyplot as plt

def parse_json(json):
    pass

def get_data():
    pass

def receive_ML(X, Y):
    pass

def make_graph(data):
    pass

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/plot/past', methods=['GET', 'POST'])
def plot_past_view(ticket):
    params = parse_json(request.json)
    X, Y = get_data(params)
    X, Y = receive_ML(X, Y)
    plotly_graph = make_graph(X, Y)
    return plotly_graph
    