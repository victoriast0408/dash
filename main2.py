import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import pandas as pd


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

df = pd.read_csv('/Users/victoria/Documents/Dashboard/dash/warengruppe.csv')
df1 = df[3:7]

app = dash.Dash()

app.layout = html.Div([
    html.H1('Dash demo'),

    dcc.Graph(
        id="sun",
        figure={ 'data':
        [go.Sunburst(
            #ids=df.warengruppe,
            labels=df1.artikel,
            parents=df1.warengruppe,
            domain=dict(column=1),
            maxdepth=1
        )]}
    )

])




if __name__ == '__main__':
    app.run_server(debug=True)