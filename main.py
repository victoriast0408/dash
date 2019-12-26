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
df3 = pd.read_csv('warengruppen_jan_fil1.csv')
df4 = pd.read_csv('warengruppen_jan_fil2.csv')
df5 = pd.read_csv('BillsFeb.csv', decimal=',')
df6 = pd.read_csv('BillsFebFil2.csv', decimal=',')
df7 = pd.read_csv('warengruppen_feb_fil1.csv')
df8 = pd.read_csv('warengruppen_feb_fil2.csv')

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

#tabs_styles = {
   # 'height': '44px'
#}

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
    name='Branch 1',
)
trace2 = go.Scatter(
    x = day_fil2,
    y = total_for_each_day_fil2,
    mode='lines+markers',
    name='Branch 2',
    line = {'color': 'rgb(147, 112, 220)'}   # change the line colour
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
    name='Branch 2',
    line={'color': 'rgb(147, 112, 220)'}
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

# Least popular

# Most popular 15 items
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

# User
labels_user_fil1 = ['Anna', 'Marie','Alex']
labels_user_fil2 = ['Andy', 'Jane', 'Mia']
total_for_each_user_jan_fil1 = df.groupby('user')['total'].sum()
total_for_each_user_jan_fil2 = df2.groupby('user')['total'].sum()
total_for_each_user_feb_fil1 = df5.groupby('user')['total'].sum()
total_for_each_user_feb_fil2 = df6.groupby('user')['total'].sum()
####

app.layout = html.Div(children=[

# Upper navigation bar
    dbc.Navbar(
        children=[
            html.H4("Family Bakery", style={'color':'white'}, className="font-weight-normal")
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
        #brand="Family Bakery",
        #brand_href="#",
        color="secondary",
        dark=True,
        className="mb-4"),

    # The second row with cards
    # Card 1
    dbc.Row([
            html.Div([
              html.Div(
                html.Div(
                  html.Div(
                    html.Div([
                        dcc.Dropdown(
                            id="dropdown-month",
                            options=[
                                {'label': 'January', 'value': 'january'},
                                {'label': 'February', 'value': 'february'},
                            ],
                            value='january',
                            clearable=False,
                        ),
                        dcc.Dropdown(
                            id="dropdown-items",
                            options=[
                                {'label': 'Branch 1', 'value': 'first'},
                                {'label': 'Branch 2', 'value': 'second'},
                            ],
                            value='first',
                            clearable=False,
                            className="mt-3"
                        ),
                    ], className="col mr-2"),
                    className="col mr-2"), className="card-body"), className="card border-left-success shadow h-100 py-2"
                    )], className="col-xl-3 col-md-3 mb-4"),


### Cards with Data

### Card 2
            html.Div([
              html.Div(
                html.Div(
                  html.Div(
                    html.Div([
                      html.Div(id='aver_content2', className="h5 mb-0 mt-4 font-weight-bold text-gray-800")], className="col mr-2"),
                        className="col mr-2"), className="card-body"), className="card border-left-info shadow h-100 py-2"
                        )], className="col-xl-3 col-md-3 mb-4"),

### Card 3
            html.Div([
              html.Div(
                html.Div(
                  html.Div(
                    html.Div(
                      html.Div(id='aver_content', className="h5 mb-0 mt-4 font-weight-bold text-gray-800"), className="col mr-2"),
                        className="col mr-2"), className="card-body"), className="card border-left-primary shadow h-100 py-2"
                        )], className="col-xl-3 col-md-3 mb-4"),


### Card 4
            html.Div([
              html.Div(
                html.Div(
                  html.Div(
                    html.Div([
                      html.Div(id='aver_content3', className="h5 mb-0 mt-4 font-weight-bold text-gray-800")], className="col mr-2"),
                        className="col mr-2"), className="card-body"), className="card border-left-warning shadow h-100 py-2"
                        )], className="col-xl-3 col-md-3 mb-4"),
]),

dbc.Row([
    dbc.Col(dbc.Card([
         dbc.CardHeader(
        html.H6('General Review', className="mx-auto pb-3 mt-4 text-center font-weight-light py-3")
         ),
        dbc.CardBody([
        html.Div(id='line-content')])
    ]), className="mt-4")

]),

dbc.Row([
    dbc.Col(dbc.Card([
        dbc.CardHeader(
        html.H6('Preferable payment method', className="mx-auto pb-3 mt-4 text-center font-weight-light")
    ),
        dbc.CardBody([
        html.Div(id='content-pie')])
    ]), className="mt-4"),
    dbc.Col(dbc.Card([
        dbc.CardHeader(
            html.H6('Sales by user', className="mx-auto pb-3 mt-4 text-center font-weight-light")
        ),
        dbc.CardBody([
            html.Div(id='user-pie')])
    ]), className="mt-4")

]),

dbc.Row([
    dbc.Col(dbc.Card([
        dbc.CardHeader(
        html.H6('TOP 15 products', className="mx-auto pb-3 mt-4 text-center font-weight-light")
    ),
        dbc.CardBody([
        html.Div(id='content-bar')])
    ]), className="mt-4")

]),

], className="container-fluid bg-light")

# For payment pie chart:
@app.callback(Output('content-pie', 'children'),
              [Input('dropdown-items', 'value'),
               Input('dropdown-month', 'value')])
def render_content(value, month_value):
    if value == "first" and month_value == 'january':
        return html.Div([
            dcc.Graph(
                id='pie_jan_1',
                figure={
                   'data': [go.Pie(labels=labels, values=values,
                                   marker={'colors': ['#0072BB', '#A0E6FE', '#9370DC']}
                                   )],
                    #'layout': {
                    #'title': 'Preferable payment method',}
                    },
                # Remove the "Produced with Plot.ly"
             config={
            "displaylogo": False,
            'modeBarButtonsToRemove': ['pan2d', 'lasso2d'],
            'displayModeBar': False        # change to True to display the modebar (plotly tools)
        },),
        ])
        # the same but for the Branch 2
    elif value == "second" and month_value == 'january':
        return html.Div([
            dcc.Graph(
                id='pie_jan_2',
                figure={
                     'data': [go.Pie(labels=labels, values=values_fil2,
                                     marker={'colors': ['#0072BB', '#A0E6FE', '#9370DC']}
                                     )],
                     'layout': {
                     #'title': 'Preferable payment method'
                         }},
                # Remove the "Produced with Plot.ly"
                config={
                    "displaylogo": False,
                    'modeBarButtonsToRemove': ['pan2d', 'lasso2d'],
                    'displayModeBar': False  # change to True to display the modebar (plotly tools)
                },
            ),
        ])
            # For February
    elif value == "first" and month_value == 'february':
        return html.Div([
            dcc.Graph(
                id='pie_feb_1',
                figure={
                    'data': [go.Pie(labels=labels, values=values_feb,
                                    marker={'colors': ['#0072BB', '#A0E6FE', '#9370DC']}
                                    )],
                    'layout': {
                        #'title': 'Preferable payment method',
                    }},
                # Remove the "Produced with Plot.ly"
                config={
                    "displaylogo": False,
                    'modeBarButtonsToRemove': ['pan2d', 'lasso2d'],
                    'displayModeBar': False  # change to True to display the modebar (plotly tools)
                }, ),
        ])
        # the same for the Branch 2
    elif value == "second" and month_value == 'february':
        return html.Div([
            dcc.Graph(
                id='pie_feb_2',
                figure={
                    'data': [go.Pie(labels=labels, values=values_feb_fil2,
                                    marker={'colors': ['#0072BB', '#A0E6FE', '#9370DC']})],
                    'layout': {
                        #'title': 'Preferable payment method'
                    }},
                # Remove the "Produced with Plot.ly"
                config={
                    "displaylogo": False,
                    'modeBarButtonsToRemove': ['pan2d', 'lasso2d'],
                    'displayModeBar': False  # change to True to display the modebar (plotly tools)
                },
            ),
        ])

# For user pie chart:
@app.callback(Output('user-pie', 'children'),
              [Input('dropdown-items', 'value'),
               Input('dropdown-month', 'value')])
def render_content(value, month_value):
    if value == "first" and month_value == 'january':
        return html.Div([
            dcc.Graph(
                id='pie_user_jan_1',
                figure={
                   'data': [go.Pie(labels=labels_user_fil1, values=total_for_each_user_jan_fil1,
                                   marker={'colors': ['#1689C9', '#12477D', '#1cc88a']}
                                   )],
                    #'layout': {
                    #'title': 'Preferable payment method',}
                    },
                # Remove the "Produced with Plot.ly"
             config={
            "displaylogo": False,
            'modeBarButtonsToRemove': ['pan2d', 'lasso2d'],
            'displayModeBar': False        # change to True to display the modebar (plotly tools)
        },),
        ])
        # the same but for the Branch 2
    elif value == "second" and month_value == 'january':
        return html.Div([
            dcc.Graph(
                id='pie_user_jan_2',
                figure={
                     'data': [go.Pie(labels=labels_user_fil2, values=total_for_each_user_jan_fil2,
                                     marker={'colors': ['#1689C9', '#12477D', '#1cc88a']}
                                     )],
                     'layout': {
                     #'title': 'Preferable payment method'
                         }},
                # Remove the "Produced with Plot.ly"
                config={
                    "displaylogo": False,
                    'modeBarButtonsToRemove': ['pan2d', 'lasso2d'],
                    'displayModeBar': False  # change to True to display the modebar (plotly tools)
                },
            ),
        ])
            # For February
    elif value == "first" and month_value == 'february':
        return html.Div([
            dcc.Graph(
                id='pie_user_feb_1',
                figure={
                    'data': [go.Pie(labels=labels_user_fil1, values=total_for_each_user_feb_fil1,
                                    marker={'colors': ['#1689C9', '#12477D', '#1cc88a']}
                                    )],
                    'layout': {
                        #'title': 'Preferable payment method',
                    }},
                # Remove the "Produced with Plot.ly"
                config={
                    "displaylogo": False,
                    'modeBarButtonsToRemove': ['pan2d', 'lasso2d'],
                    'displayModeBar': False  # change to True to display the modebar (plotly tools)
                }, ),
        ])
        # the same for the Branch 2
    elif value == "second" and month_value == 'february':
        return html.Div([
            dcc.Graph(
                id='pie_user_feb_2',
                figure={
                    'data': [go.Pie(labels=labels_user_fil2, values=total_for_each_user_feb_fil2,
                                    marker={'colors': ['#1689C9', '#12477D', '#1cc88a']})],
                    'layout': {
                        #'title': 'Preferable payment method'
                    }},
                # Remove the "Produced with Plot.ly"
                config={
                    "displaylogo": False,
                    'modeBarButtonsToRemove': ['pan2d', 'lasso2d'],
                    'displayModeBar': False  # change to True to display the modebar (plotly tools)
                },
            ),
        ])

# For TOP 15 bars:
@app.callback(Output('content-bar', 'children'),
              [Input('dropdown-items', 'value'),
               Input('dropdown-month', 'value')])
def render_content(value, month_value):
    if value == "first" and month_value == 'january':
        return html.Div([
            dcc.Graph(
                id='graph-1-1-tabs',
                 figure={
                     'data': [go.Bar(x= most_pop_item_fil1, y=most_pop_item_count_fil1,
                                     marker={'color': most_pop_item_count_feb_fil1,
                                             'colorscale': ['#f2fcfe', '#1c92d2']}
                                    )],
                     'layout':{
                     #'title': 'Most popular 15 items',
                     'yaxis': {'title': 'Number of sold items'}}},
                 # Remove the "Produced with Plot.ly"
                 config={
                     "displaylogo": False,
                     'modeBarButtonsToRemove': ['pan2d', 'lasso2d'],
                     'displayModeBar': False  # change to True to display the modebar (plotly tools)
                 }, )
        ])
        # the same but for the Branch 2
    elif value == "second" and month_value == 'january':
        return html.Div([
             dcc.Graph(
                 id='graph-2-2-tabs',
                 figure={
                     'data': [go.Bar(x=most_pop_item_fil2, y=most_pop_item_count_fil2,
                                     marker={'color': most_pop_item_count_feb_fil1,
                                            'colorscale': ['#f2fcfe', '#1c92d2']}
                                     )],
                     'layout': {
                         #'title': 'Most popular 15 items',
                         'yaxis': {'title': 'Number of sold items'}}},
                 # Remove the "Produced with Plot.ly"
                 config={
                     "displaylogo": False,
                     'modeBarButtonsToRemove': ['pan2d', 'lasso2d'],
                     'displayModeBar': False  # change to True to display the modebar (plotly tools)
                 }, )
        ])
            # For February
    elif value == "first" and month_value == 'february':
        return html.Div([
             dcc.Graph(
                 id='graph-1-1-tabs',
                 figure={
                     'data': [go.Bar(x=most_pop_item_feb_fil1, y=most_pop_item_count_feb_fil1,
                                     marker={'color': most_pop_item_count_feb_fil1,
                                             #'colorscale': 'ylorrd'}        --> standart colorscale
                                             #'colorscale':[[0, 'green'], [0.5, 'red'], [1.0, 'rgb(0, 0, 255)']]}  --> differnet colors
                                             'colorscale': ['#f2fcfe', '#1c92d2']}
                                     )],
                     'layout': {
                         #'title': 'Most popular 15 items',
                         'yaxis': {'title': 'Number of sold items'}}},
                 # Remove the "Produced with Plot.ly"
                 config={
                     "displaylogo": False,
                     'modeBarButtonsToRemove': ['pan2d', 'lasso2d'],
                     'displayModeBar': False  # change to True to display the modebar (plotly tools)
                 }, )
        ])
        # the same for the Branch 2
    elif value == "second" and month_value == 'february':
        return html.Div([
             dcc.Graph(
                 id='graph-2-2-tabs',
                 figure={
                    'data': [go.Bar(x=most_pop_item_feb_fil2, y=most_pop_item_count_feb_fil2,
                                     marker={'color': most_pop_item_count_feb_fil1,
                                             'colorscale': ['#f2fcfe', '#1c92d2']}
                                     )],
                     'layout': {
                         #'title': 'Most popular 15 items',
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
            [Input('dropdown-items', 'value'),
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
            [Input('dropdown-items', 'value'),
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
                    #'title':'Total amount per day',
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
