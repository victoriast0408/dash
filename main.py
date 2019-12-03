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
        color="#293843",
        dark=True,
    ),

    # The second row with cards
    dbc.Row([

            html.Div([
              html.Div(
                html.Div(
                  html.Div(
                    html.Div([
                      html.Div("Today: ", className="text-xs font-weight-bold text-primary text-uppercase mb-1"),
                      html.Div("30 January 2020", className="h5 mb-0 font-weight-bold text-gray-800")], className="col mr-2"),
                    className="col mr-2"), className="card-body"), className="card border-left-primary shadow h-100 py-2"
                    )], className="col-xl-3 col-md-3 mb-4 mt-3"),

### Cards with Radio buttons
            html.Div([
              html.Div(
                html.Div(
                  html.Div(
                    html.Div([
                    dcc.RadioItems(
                        id="radio-items",
                        options =[
                            {'label':'Branch 1' ,'value': 'first'},
                            {'label': 'Branch 2', 'value': 'second'}
                      ], value = "first", 
                        labelStyle={'display': 'inline-block'}, className="mr-4"),
                      html.Div(id='aver_content', className="h5 mb-0 font-weight-bold text-gray-800")], className="col mr-2"),
                        className="col mr-2"), className="card-body"), className="card border-left-primary shadow h-100 py-2"
                        )], className="col-xl-3 col-md-3 mb-4 mt-3"),


### Radio buttons 2
            html.Div([
              html.Div(
                html.Div(
                  html.Div(
                    html.Div([
                    dcc.RadioItems(
                        id="radio-items2",
                        options =[
                            {'label':'Branch 1' ,'value': 'first'},
                            {'label': 'Branch 2', 'value': 'second'}
                      ], value = "first",
                        labelStyle={'display': 'inline-block'}),
                      html.Div(id='aver_content2', className="h5 mb-0 font-weight-bold text-gray-800")], className="col mr-2"),
                        className="col mr-2"), className="card-body"), className="card border-left-primary shadow h-100 py-2"
                        )], className="col-xl-3 col-md-3 mb-4 mt-3"),


### Radio buttons 3
            html.Div([
              html.Div(
                html.Div(
                  html.Div(
                    html.Div([
                    dcc.RadioItems(
                        id="radio-items3",
                        options =[
                            {'label':'Branch 1' ,'value': 'first'},
                            {'label': 'Branch 2', 'value': 'second'}
                      ], value = "first",
                        labelStyle={'display': 'inline-block'}),
                      html.Div(id='aver_content3', className="h5 mb-0 font-weight-bold text-gray-800")], className="col mr-2"),
                        className="col mr-2"), className="card-body"), className="card border-left-primary shadow h-100 py-2"
                        )], className="col-xl-3 col-md-3 mb-4 mt-3"),
]),



#dbc.Row(html.H3('General Review', className="mx-auto pt-3")),

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
    ), className = "border-left-primary shadow"))),

html.H1(children= ''), # Empty div as a separator

#dbc.Row(html.H3('Additional Information', className="mx-auto pb-3")),

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

], className="container-fluid bg-light")

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

# For average bills radio
@app.callback(Output('aver_content', 'children'),
            [Input('radio-items', 'value')])
def update_radio_item_output(value):
    if value == "first":
        return html.Div([
                 html.H4("Average Bill pro Month: "),
                 html.H4(df['total'].mean().round(2))
            ], className="text-center")
    elif value == "second":
        return html.Div([
               html.H4("Average Bill pro Month: "),
                html.H4(df2['total'].mean().round(2))
            ], className="text-center")

# For number of bills radio
@app.callback(Output('aver_content2', 'children'),
            [Input('radio-items2', 'value')])
def update_radio_item_output2(value):
    if value == "first":
        return html.Div([
                        html.H4("Number of Bills pro Month: "),
                        html.H4(df['bill_number'].count())
                    ], className="text-center")
    elif value == "second":
        return html.Div([
                         html.H4("Number of Bills pro Month: "),
                         html.H4(df2['bill_number'].count())
                    ], className="text-center")

# For total pro month radio
@app.callback(Output('aver_content3', 'children'),
            [Input('radio-items3', 'value')])
def update_radio_item_output3(value):
    if value == "first":
        return html.Div([
            html.H4("Total amount pro Month: "),
            html.H4(df['total'].sum())
        ], className="text-center")
    elif value == "second":
        return html.Div([
            html.H4("Total amount pro Month: "),
            html.H4(df2['total'].sum())
        ], className="text-center")

    ####

    
# TO DO:
# Navigation bar
# Radio buttons margin
# Graphs styling
# Bar gradient color

if __name__ == '__main__':
    app.run_server()
