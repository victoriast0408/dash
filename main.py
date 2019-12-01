from datetime import datetime as dt
import dash
import dash_bootstrap_components as dbc
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
df3 = pd.read_csv('warengruppen_fil1.csv')
df4 = pd.read_csv('warengruppen_fil2.csv')

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

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
    name='Branch 1'
)
trace2 = go.Scatter(
    x = day_fil2,
    y = total_for_each_day_fil2,
    mode='lines+markers',
    name='Branch 2'
)
####


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

# Most popular 15 items
df_most_pop_item_fil1 = df3.nlargest(15, ['anzahl'])
most_pop_item_fil1 = df_most_pop_item_fil1['artikel']
most_pop_item_count_fil1 = df_most_pop_item_fil1['anzahl']

df_most_pop_item_fil2 = df4.nlargest(15, ['anzahl'])
most_pop_item_fil2 = df_most_pop_item_fil2['artikel']
most_pop_item_count_fil2 = df_most_pop_item_fil2['anzahl']
####
app.layout = html.Div(children=[

    # Upper navigation bar
    dbc.NavbarSimple(
        children=[
            #dbc.NavItem(dbc.NavLink("Page 1", href="#")),
            dbc.DropdownMenu(
                children=[
                    dbc.DropdownMenuItem("More pages", header=True),
                ],
                nav=True,
                in_navbar=True,
                label="More",
            ),
        ],
        brand="Family Bakery",
        brand_href="#",
        color="secondary",
        dark=True,
    ),

    # The second row with cards
    dbc.Row([
                    dbc.Col(
                        dbc.Card([
                            dbc.CardHeader(html.H3("Today: ", className="card-title")),
                            dbc.CardBody(
                                [
                                    html.H4('30 January 2020', className="text-center")
                                    #dbc.CardLink("Card link", href="#"),
                                    #dbc.CardLink("External link", href="https://google.com"),
                                ]
                            ),
                            #style={"width": "18rem"},
                        ], className="card h-100")
                    ),
                    dbc.Col(dbc.Card([
                            dbc.CardHeader(
                                    dcc.Tabs(id="tabs-aver-bill", value='tab-1-aver-bill', children=[
                                        dcc.Tab(label='Branch 1', value='tab-1-aver-bill'),
                                        dcc.Tab(label='Branch 2', value='tab-2-aver-bill'),
                                    ]),
                            ),
                            dbc.CardBody(
                                    # container for new data in tab:
                                    html.Div(id='tabs-aver-bill-content')
                            ),
                            #style={"width": "18rem", "height":"300px"},
                        ])),

                    dbc.Col(dbc.Card([
                        dbc.CardHeader(
                                dcc.Tabs(id="tabs-count-bill", value='tab-1-count-bill', children=[
                                    dcc.Tab(label='Branch 1', value='tab-1-count-bill'),
                                    dcc.Tab(label='Branch 2', value='tab-2-count-bill'),
                                ]),
                            ),
                        dbc.CardBody(
                               # container for new data in tab:
                                html.Div(id='tabs-count-bill-content'),
                        ),
                        #style={"width": "18rem", "height": "300px"},
                    ])),
                ], className='pt-3'),


    dbc.Row(html.H3('General Review', className="mx-auto pt-3")),

    dbc.Row(dbc.Col(html.Div(
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
    )))),

    html.H1(children= ''), # Empty div as a separator

    dbc.Row(html.H3('Additional Information', className="mx-auto pb-3")),

    dbc.Row([
    dbc.Col(dbc.Card([
        dbc.CardHeader(
    dcc.Tabs(id="tabs-example", value='tab-1-example', children=[
        dcc.Tab(label='Branch 1', value='tab-1-example'),
        dcc.Tab(label='Branch 2', value='tab-2-example'),
    ])),
        dbc.CardBody([
        #container for new pie according to the selected tab:
        html.Div(id='tabs-content-example')])
    ]))
])

], className="container-fluid")

# For tabs
@app.callback(Output('tabs-content-example', 'children'),
              [Input('tabs-example', 'value')])
def render_content(tab):
    if tab == 'tab-1-example':
        return html.Div([
            dcc.Graph(
                id='graph-1-tabs',
                figure={
                   'data': [go.Pie(labels=labels, values=values)],
                    'layout': {
                    'title': 'Preferable payment method',
                }},
                # Remove the "Produced with Plot.ly"
             config={
            "displaylogo": False,
            'modeBarButtonsToRemove': ['pan2d', 'lasso2d'],
            'displayModeBar': False        # change to True to display the modebar (plotly tools)
        },),
            # "15 most popular items" graph
            dcc.Graph(
                id='graph-1-1-tabs',
                figure={
                    'data': [go.Bar(x= most_pop_item_fil1, y=most_pop_item_count_fil1)],
                    'layout':{
                    'title': 'Most popular 15 items',
                    'yaxis': {'title': 'Number of sold items'}}},
                # Remove the "Produced with Plot.ly"
                config={
                    "displaylogo": False,
                    'modeBarButtonsToRemove': ['pan2d', 'lasso2d'],
                    'displayModeBar': False  # change to True to display the modebar (plotly tools)
                }, )
        ])
    elif tab == 'tab-2-example':
        return html.Div([
            dcc.Graph(
                id='graph-2-tabs',
                figure={
                     'data': [go.Pie(labels=labels, values=values_fil2)],
                     'layout': {
                     'title': 'Preferable payment method'}},
                # Remove the "Produced with Plot.ly"
                config={
                    "displaylogo": False,
                    'modeBarButtonsToRemove': ['pan2d', 'lasso2d'],
                    'displayModeBar': False  # change to True to display the modebar (plotly tools)
                },
            ),
            # "15 most popular items" graph
            dcc.Graph(
                id='graph-2-2-tabs',
                figure={
                    'data': [go.Bar(x=most_pop_item_fil2, y=most_pop_item_count_fil2)],
                    'layout': {
                        'title': 'Most popular 15 items',
                        'yaxis': {'title': 'Number of sold items'}}},
                # Remove the "Produced with Plot.ly"
                config={
                    "displaylogo": False,
                    'modeBarButtonsToRemove': ['pan2d', 'lasso2d'],
                    'displayModeBar': False  # change to True to display the modebar (plotly tools)
                }, )
        ])

# For average bills tabs
@app.callback(Output('tabs-aver-bill-content', 'children'),
            [Input('tabs-aver-bill', 'value')])
def render_content_aver_bill(aver_bill_tab):
    if aver_bill_tab == 'tab-1-aver-bill':
        return html.Div([
                html.H4("Average Bill pro Month: "),
                html.H4(df['total'].mean().round(2))
            ], className="text-center")
    elif aver_bill_tab == 'tab-2-aver-bill':
        return html.Div([
                html.H4("Average Bill pro Month: "),
                html.H4(df2['total'].mean().round(2))
            ], className="text-center")

# For count bills tabs
@app.callback(Output('tabs-count-bill-content', 'children'),
            [Input('tabs-count-bill', 'value')])
def render_content_count_bill(count_bill_tab):
    if count_bill_tab == 'tab-1-count-bill':
        return html.Div([
                html.H4("Number of Bills pro Month: "),
                html.H4(df['bill_number'].count())
            ], className="text-center")
    elif count_bill_tab == 'tab-2-count-bill':
        return html.Div([
                html.H4("Number of Bills pro Month: "),
                html.H4(df2['bill_number'].count())
            ], className="text-center")

    ####

if __name__ == '__main__':
    app.run_server()
