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
df5 = pd.read_csv('BillsFeb.csv', decimal=',')
df6 = pd.read_csv('BillsFebFil2.csv', decimal=',')
df7 = pd.read_csv('warengruppen_feb_fil1.csv')
df8 = pd.read_csv('warengruppen_feb_fil2.csv')

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Group by days and store the unique values in 'day' for January
day = df['date'].unique()
day_fil2 = df2['date'].unique()
# and for February
day_feb = df5['date'].unique()
day_feb_fil2 = df6['date'].unique()

# Group by date and get the sum of 'total' column for every day January
total_for_each_day = df.groupby('date')['total'].sum()
total_for_each_day_fil2 = df2.groupby('date')['total'].sum()
# and for February
total_for_each_day_feb = df5.groupby('date')['total'].sum()
total_for_each_day_fil2_feb = df6.groupby('date')['total'].sum()

# Create traces for id=line: trace1= Filial 1 and trace2= Filial2 for January
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

# Create traces for id=line: trace3= Filial 1 and trace4= Filial2 for February
trace3 = go.Scatter(
    x = day_feb,
    y = total_for_each_day_feb,
    mode='lines+markers',
    name='Branch 1'
)
trace4 = go.Scatter(
    x = day_feb_fil2,
    y = total_for_each_day_fil2_feb,
    mode='lines+markers',
    name='Branch 2'
)
####


# Create labels and values for id=pie for January
labels = ['Cash', 'Credit Card','Customer Card']

paid_cash_sum = df['paid_cash'].sum()
paid_card_sum = df['paid_card'].sum()
paid_customer_card_sum = df['paid_customer_card'].sum()
values = [paid_cash_sum, paid_card_sum, paid_customer_card_sum]

paid_cash_sum_fil2 = df2['paid_cash'].sum()
paid_card_sum_fil2 = df2['paid_card'].sum()
paid_customer_card_sum_fil2 = df2['paid_customer_card'].sum()
values_fil2 = [paid_cash_sum_fil2, paid_card_sum_fil2, paid_customer_card_sum_fil2]

# and for February
paid_cash_sum_feb = df5['paid_cash'].sum()
paid_card_sum_feb = df5['paid_card'].sum()
paid_customer_card_sum_feb = df5['paid_customer_card'].sum()
values_feb = [paid_cash_sum_feb, paid_card_sum_feb, paid_customer_card_sum_feb]

paid_cash_sum_feb_fil2 = df6['paid_cash'].sum()
paid_card_sum_feb_fil2 = df6['paid_card'].sum()
paid_customer_card_sum_feb_fil2 = df6['paid_customer_card'].sum()
values_feb_fil2 = [paid_cash_sum_feb_fil2, paid_card_sum_feb_fil2, paid_customer_card_sum_feb_fil2]
####

# Most popular 15 items for January:
df_most_pop_item_fil1 = df3.nlargest(15, ['anzahl'])
most_pop_item_fil1 = df_most_pop_item_fil1['artikel']
most_pop_item_count_fil1 = df_most_pop_item_fil1['anzahl']

df_most_pop_item_fil2 = df4.nlargest(15, ['anzahl'])
most_pop_item_fil2 = df_most_pop_item_fil2['artikel']
most_pop_item_count_fil2 = df_most_pop_item_fil2['anzahl']
# and for February:
df_most_pop_item_feb_fil1 = df7.nlargest(15, ['anzahl'])
most_pop_item_feb_fil1 = df_most_pop_item_feb_fil1['artikel']
most_pop_item_count_feb_fil1 = df_most_pop_item_feb_fil1['anzahl']

df_most_pop_item_feb_fil2 = df8.nlargest(15, ['anzahl'])
most_pop_item_feb_fil2 = df_most_pop_item_feb_fil2['artikel']
most_pop_item_count_feb_fil2 = df_most_pop_item_feb_fil2['anzahl']
####
app.layout = html.Div(children=[

    # Upper navigation bar
    dbc.NavbarSimple(
        children=[
            html.Div("Select month: ", style={'color': 'white', 'fontSize': 11}),
            dcc.Dropdown(
                        id="dropdown-month",
                        options=[
                            {'label': 'January', 'value': 'january'},
                            {'label': 'February', 'value': 'february'},
                        ],
                        value='january',
                        clearable=False,
                    ),
            #dbc.NavItem(dbc.NavLink("Page 1", href="#")),
            #dbc.DropdownMenu(
                #children=[
                    #dbc.DropdownMenuItem("More pages", header=True),
                #],
                #nav=True,
                #in_navbar=True,
                #label="More",
            #),
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
                      html.Div("28 February", className="h5 mb-0 font-weight-bold text-gray-800"),
                    ], className="col mr-2"),
                    className="col mr-2"), className="card-body"), className="card border-left-primary shadow h-100 py-2"
                    )], className="col-xl-3 col-md-3 mb-4 mt-3"),

### Cards with Dropdowv
            html.Div([
              html.Div(
                html.Div(
                  html.Div(
                    html.Div([
                    dcc.Dropdown(
                        id="dropdown-items",
                        options=[
                            {'label': 'Branch 1', 'value': 'first'},
                            {'label': 'Branch 2', 'value': 'second'},
                        ],
                        value='first',
                        clearable=False,
                    ),
                      html.Div(id='aver_content', className="h5 mb-0 font-weight-bold text-gray-800")], className="col mr-2"),
                        className="col mr-2"), className="card-body"), className="card border-left-primary shadow h-100 py-2"
                        )], className="col-xl-3 col-md-3 mb-4 mt-3"),


### Dropdown buttons 2
            html.Div([
              html.Div(
                html.Div(
                  html.Div(
                    html.Div([
                        dcc.Dropdown(
                            id="dropdown-items2",
                            options=[
                                {'label': 'Branch 1', 'value': 'first'},
                                {'label': 'Branch 2', 'value': 'second'},
                            ],
                            value='first',
                            clearable=False,
                        ),
                      html.Div(id='aver_content2', className="h5 mb-0 font-weight-bold text-gray-800")], className="col mr-2"),
                        className="col mr-2"), className="card-body"), className="card border-left-primary shadow h-100 py-2"
                        )], className="col-xl-3 col-md-3 mb-4 mt-3"),


### Dropdown buttons 3
            html.Div([
              html.Div(
                html.Div(
                  html.Div(
                    html.Div([
                        dcc.Dropdown(
                            id="dropdown-items3",
                            options=[
                                {'label': 'Branch 1', 'value': 'first'},
                                {'label': 'Branch 2', 'value': 'second'},
                            ],
                            value='first',
                            clearable=False,
                        ),
                      html.Div(id='aver_content3', className="h5 mb-0 font-weight-bold text-gray-800")], className="col mr-2"),
                        className="col mr-2"), className="card-body"), className="card border-left-primary shadow h-100 py-2"
                        )], className="col-xl-3 col-md-3 mb-4 mt-3"),
]),



#dbc.Row(html.H3('General Review', className="mx-auto pt-3")),

dbc.Row(dbc.Col(html.Div(
    # container for new pie according to the selected tab:
    html.Div(id='line-content')))),
#html.H1(children= ''), # Empty div as a separator

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
]),
], className="container-fluid bg-light")


# For tabs
@app.callback(Output('tabs-content-example', 'children'),
              [Input('tabs-example', 'value'),
               Input('dropdown-month', 'value')])
def render_content(tab, month_value):
    if tab == 'tab-1-example' and month_value == 'january':
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
    elif tab == 'tab-2-example' and month_value == 'january':
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

    elif tab == 'tab-1-example' and month_value == 'february':
        return html.Div([
            dcc.Graph(
                id='graph-1-tabs',
                figure={
                    'data': [go.Pie(labels=labels, values=values_feb)],
                    'layout': {
                        'title': 'Preferable payment method',
                    }},
                # Remove the "Produced with Plot.ly"
                config={
                    "displaylogo": False,
                    'modeBarButtonsToRemove': ['pan2d', 'lasso2d'],
                    'displayModeBar': False  # change to True to display the modebar (plotly tools)
                }, ),
            # "15 most popular items" graph
            dcc.Graph(
                id='graph-1-1-tabs',
                figure={
                    'data': [go.Bar(x=most_pop_item_fil1, y=most_pop_item_count_feb_fil1)],
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
    elif tab == 'tab-2-example' and month_value == 'february':
        return html.Div([
            dcc.Graph(
                id='graph-2-tabs',
                figure={
                    'data': [go.Pie(labels=labels, values=values_feb_fil2)],
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
                    'data': [go.Bar(x=most_pop_item_fil2, y=most_pop_item_count_feb_fil2)],
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

# For average bills dropdown
@app.callback(Output('aver_content', 'children'),
            [Input('dropdown-items', 'value'),
             Input('dropdown-month', 'value')])
def update_dropdown_item_output(value, month_value):
    if value == "first" and month_value == "january":
        return html.Div([
                 html.H4("Average Bill: "),
                 html.H4(df['total'].mean().round(2))
            ], className="text-center")
    elif value == "second" and month_value == "january":
        return html.Div([
               html.H4("Average Bill: "),
                html.H4(df2['total'].mean().round(2))
            ], className="text-center")
    elif value == "first" and month_value == "february":
        return html.Div([
                 html.H4("Average Bill: "),
                 html.H4(df5['total'].mean().round(2))
            ], className="text-center")
    elif value == "second" and month_value == "february":
        return html.Div([
               html.H4("Average Bill: "),
               html.H4(df6['total'].mean().round(2))
            ], className="text-center")

# For number of bills dropdown
@app.callback(Output('aver_content2', 'children'),
            [Input('dropdown-items2', 'value'),
             Input('dropdown-month', 'value')])
def update_rdropdown_item_output2(value, month_value):
    if value == "first" and month_value == "january":
        return html.Div([
                        html.H4("Number of Bills: "),
                        html.H4(df['bill_number'].count())
                    ], className="text-center")
    elif value == "second" and month_value == "january":
        return html.Div([
                         html.H4("Number of Bills: "),
                         html.H4(df2['bill_number'].count())
                    ], className="text-center")
    elif value == "first" and month_value == "february":
        return html.Div([
                        html.H4("Number of Bills: "),
                        html.H4(df5['bill_number'].count())
                    ], className="text-center")
    elif value == "second" and month_value == "february":
        return html.Div([
                         html.H4("Number of Bills: "),
                         html.H4(df6['bill_number'].count())
                    ], className="text-center")

# For total pro month dropdown
@app.callback(Output('aver_content3', 'children'),
            [Input('dropdown-items3', 'value'),
             Input('dropdown-month', 'value')])
def update_dropdown_item_output3(value, month_value):
    if value == "first" and month_value == "january":
        return html.Div([
            html.H4("Total amount: "),
            html.H4(df['total'].sum())
        ], className="text-center")
    elif value == "second" and month_value == "january":
        return html.Div([
            html.H4("Total amount: "),
            html.H4(df2['total'].sum())
        ], className="text-center")
    elif value == "first" and month_value == "february":
        return html.Div([
            html.H4("Total amount: "),
            html.H4(df5['total'].sum())
        ], className="text-center")
    elif value == "second" and month_value == "february":
        return html.Div([
            html.H4("Total amount: "),
            html.H4(df6['total'].sum())
        ], className="text-center")

# For line graph
@app.callback(Output('line-content', 'children'),
            [Input('dropdown-month', 'value')])
def update_line_graph(month_value):
    if month_value == "january":
        return html.Div([
            dcc.Graph(
                id="line_jan",
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
                    'displayModeBar': False  # change to True to display the modebar (plotly tools)
                },
            )
            ])
    elif month_value == "february":
        return html.Div([
            dcc.Graph(
                id="line_feb",
                figure= {
                    'data': [trace3, trace4],
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
                    'displayModeBar': False  # change to True to display the modebar (plotly tools)
                },
            )
            ])

    
# TO DO:
# add .csv for Feb for Branch 2
# Navigation bar
# Graphs styling
# Bar gradient color




if __name__ == '__main__':
    app.run_server()
