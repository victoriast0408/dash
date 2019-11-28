from datetime import datetime as dt
import dash
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import plotly.offline as pyo

# read the file and replace the comma with dot in decimal
df = pd.read_csv('BillsJan.csv', decimal=',')
df2 = pd.read_csv('BillsJanFil2.csv', decimal=',')

app = dash.Dash()

# Group by days and store the unique values in 'day'
day = df['date'].unique()
day_fil2 = df2['date'].unique()

# Group by date and get the sum of 'total' column for every day
total_for_each_day = df.groupby('date')['total'].sum()
total_for_each_day_fil2 = df2.groupby('date')['total'].sum()

# Create traces for id=line: trace1= Filial 1 and trace2= Filial2
trace1 = go.Scatter(
    x = day,
    y = total_for_each_day,
    mode='lines+markers',
    name='Filial 1'
)
trace2 = go.Scatter(
    x = day_fil2,
    y = total_for_each_day_fil2,
    mode='lines+markers',
    name='Filial 2'
)
####

filials = ['Filial 1', 'Filial 2']


# Create labels and values for id=pie
labels = ['Cash', 'Credit Card','Customer Card']

paid_cash_sum = df['paid_cash'].sum()
paid_card_sum = df['paid_card'].sum()
paid_customer_card_sum = df['paid_customer_card'].sum()
values = [paid_cash_sum, paid_card_sum, paid_customer_card_sum]

paid_cash_sum_fil2 = df2['paid_cash'].sum()
paid_card_sum_fil2 = df2['paid_card'].sum()
paid_customer_card_sum_fil2 = df2['paid_customer_card'].sum()
values_fil2 = [paid_cash_sum_fil2, paid_card_sum_fil2, paid_customer_card_sum_fil2]
####




app.layout = html.Div(children=[
    html.H1(children= 'Family Bakery'),
    html.H3(children= 'General Review'),

    dcc.Graph(
        id="line",
        figure= {
            'data': [trace1, trace2],
            'layout':{
                'title':'Total amount per day',
                'showlegend': True,
                #'xaxis': {'title': 'Days', 'titlefont':{
                                            #'family':'Arial, sans-serif',
                                            #'size':18,
                                            #'color':'red',}},
                'yaxis': {'title': 'Total in CHF'},
            },
        },
        # Remove the "Produced with Plot.ly"
        config={
            "displaylogo": False,
            'modeBarButtonsToRemove': ['pan2d', 'lasso2d'],
            'displayModeBar': False        # change to True to display the modebar (plotly tools)
        },
    ),

    html.H1(children= ''),
    html.H3('Preferable payment method'),
    dcc.Tabs(id="tabs-example", value='tab-1-example', children=[
        dcc.Tab(label='Filial 1', value='tab-1-example'),
        dcc.Tab(label='Filial 2', value='tab-2-example'),
    ]),
    html.Div(id='tabs-content-example')


])

# For tabs
@app.callback(Output('tabs-content-example', 'children'),
              [Input('tabs-example', 'value')])
def render_content(tab):
    if tab == 'tab-1-example':
        return html.Div([
            #html.H3('Tab content 1'),
            dcc.Graph(
                id='graph-1-tabs',
                figure={
                   'data': [go.Pie(labels=labels, values=values)]
                    
                }
            )
        ])
    elif tab == 'tab-2-example':
        return html.Div([
            #html.H3('Tab content 2'),
            dcc.Graph(
                id='graph-2-tabs',
                figure={
                     'data': [go.Pie(labels=labels, values=values_fil2)]
                    
                }
            )
        ])

    ####

if __name__ == '__main__':
    app.run_server()
