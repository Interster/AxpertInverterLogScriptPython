import pandas as pd
import csv
import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import random
import plotly.graph_objs as go
from collections import deque

with open("aqua.csv", "r") as f:
       temp_last_line = f.readlines()[-1].strip().split(",")
       #temp_secondlast_line = f.readlines()[-2].strip().split(",")
X = deque(maxlen=100)
X.append(temp_last_line)
X.append(temp_last_line)
Y = deque(maxlen=100)
Y.append("0")
Y.append("100")

app = dash.Dash(__name__)
app.layout = html.Div(
    [
        dcc.Graph(id='live-graph', animate=True),
        dcc.Interval(
            id='graph-update',
            interval=1*10000
        ),
    ]
)

@app.callback(Output('live-graph', 'figure'),
            [Input('graph-update', 'n_intervals')]
            )
def update_graph_scatter(self):
    with open("aqua.csv", "r") as f:
         last_line = f.readlines()[-1].strip().split(",")
    if  str(X[-1]) == str(last_line[1]):
        print("same shit")
    else: 
        X.append(last_line[1])
        Y.append(last_line[2])
        print(X)
        print(Y)
        data = plotly.graph_objs.Scatter(
                x=list(X),
                y=list(Y),
                name='Scatter',
                mode= 'lines+markers'
                )
        return {'data': [data],'layout' : go.Layout(xaxis=dict(range=[min(X),max(X)]),
                                                yaxis=dict(range=[min(Y),100]),)}



if __name__ == '__main__':
    app.run_server(debug=True)


