#%%
# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
# -----------------------------------------------------------------------------
# Importing the modules
# -----------------------------------------------------------------------------
import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc

import pandas as pd
import plotly.express as px


#global current_temperature
#current_temperature = "NaN"

#%%

# -----------------------------------------------------------------------------
# Defining Dash app
# -----------------------------------------------------------------------------
app = dash.Dash(external_stylesheets=[dbc.themes.DARKLY])

# -----------------------------------------------------------------------------
# Temperature card
# -----------------------------------------------------------------------------
card = dbc.Card(
    html.H4(id="temperature")
)

buttons = html.Div(
    [
        dbc.Button("Primary", color="primary", className="me-1"),
        dbc.Button("Secondary", color="secondary", className="me-1"),
        dbc.Button("Success", color="success", className="me-1"),
        dbc.Button("Warning", color="warning", className="me-1"),
        dbc.Button("Danger", color="danger", className="me-1"),
        dbc.Button("Info", color="info", className="me-1"),
        dbc.Button("Light", color="light", className="me-1"),
        dbc.Button("Dark", color="dark", className="me-1"),
        dbc.Button("Link", color="link"),
    ]
)

df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")


# -----------------------------------------------------------------------------
# Application layout
# -----------------------------------------------------------------------------
app.layout = dbc.Container(
    [
        dcc.Interval(id='update', n_intervals=0, interval=1000*3),
        html.H1("Monitoring IoT Sensor Data with Plotly Dash"),
        html.Hr(),
        dbc.Row(dbc.Col(card, lg=4)),
        html.H1("Ekstra opskrif"),
        buttons,
        
        dcc.Graph(
        id='example-graph',
        figure=fig
        )
    ]
)


# -----------------------------------------------------------------------------
# Callback for updating temperature data
# -----------------------------------------------------------------------------
@app.callback(
    Output('temperature', 'children'),
    Input('update', 'n_intervals')
)

def update_temperature(timer):
    current_temperature = 35
    return ("Temperature: " + str(current_temperature))


# -----------------------------------------------------------------------------
# Main function
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    app.run_server(debug=True)