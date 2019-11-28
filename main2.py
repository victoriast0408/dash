import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import pandas as pd


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

df = pd.read_csv('BillsJan.csv', decimal=',')
df2 = pd.read_csv('BillsJanFil2.csv', decimal=',')

app = dash.Dash()

labels = ['Cash', 'Credit Card','Customer Card']

paid_cash_sum = df['paid_cash'].sum()
paid_card_sum = df['paid_card'].sum()
paid_customer_card_sum = df['paid_customer_card'].sum()
values = [paid_cash_sum, paid_card_sum, paid_customer_card_sum]

paid_cash_sum_fil2 = df2['paid_cash'].sum()
paid_card_sum_fil2 = df2['paid_card'].sum()
paid_customer_card_sum_fil2 = df2['paid_customer_card'].sum()
values_fil2 = [paid_cash_sum_fil2, paid_card_sum_fil2, paid_customer_card_sum_fil2]

app.layout = html.Div([
    html.H1('Dash Tabs component demo'),
    dcc.Tabs(id="tabs-example", value='tab-1-example', children=[
        dcc.Tab(label='Tab One', value='tab-1-example'),
        dcc.Tab(label='Tab Two', value='tab-2-example'),
    ]),
    html.Div(id='tabs-content-example')
])


@app.callback(Output('tabs-content-example', 'children'),
              [Input('tabs-example', 'value')])
def render_content(tab):
    if tab == 'tab-1-example':
        return html.Div([
            html.H3('Tab content 1'),
            dcc.Graph(
                id='graph-1-tabs',
                figure={
                   'data': [go.Pie(labels=labels, values=values)]
                    
                }
            )
        ])
    elif tab == 'tab-2-example':
        return html.Div([
            html.H3('Tab content 2'),
            dcc.Graph(
                id='graph-2-tabs',
                figure={
                     'data': [go.Pie(labels=labels, values=values_fil2)]
                    
                }
            )
        ])


if __name__ == '__main__':
    app.run_server(debug=True)