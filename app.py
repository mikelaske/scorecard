"""
Scorecard Dashboard

# DataTable Example #1 -- Trending Twitter https://github.com/eliasdabbas/trending-twitter/blob/master/app.py
# DataTable Example #2 -- Twitter Dash https://github.com/eliasdabbas/twitterdash/blob/master/app.py
"""

# Imports
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash_table import DataTable
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd

# Settings
# -*- coding: utf-8 -*-
pd.set_option('display.max_columns', 20)
pd.set_option('display.float_format', lambda x: '%.2f' % x)

#########################
# APP
#########################

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Deploy to Server
server = app.server

#########################
# DATA
#########################

df = pd.read_csv('data/scorecard_file.csv', encoding='unicode_escape')
df.set_index('SecId', inplace=True)

# Lists
features = df.columns
category_list = df['Category'].unique()
category_count = df['Category'].nunique()

#########################
# LAYOUT
#########################

app.layout = dbc.Container([
    html.Br(),
    html.H1('Fund Comparisons', style={'textAlign': 'center'}),
    html.Br(),
    # INPUTS
    dbc.Row([
        dbc.Col(lg=1),
        dbc.Col([
            dcc.Dropdown(id='category_id',
                         placeholder='Select Category',
                         options=[{'label': loc, 'value': i} for i, loc in enumerate(category_list)]),
        ], lg=3),
            dcc.RadioItems(id='activepassive_id',
                           options=[{'label': i, 'value': i} for i in df['Active-Passive'].unique()],
                           value='Active'),
        html.Br(),
    # BUTTON
        dbc.Col([
            dbc.Button(id='submit_button',
                       children='Submit',
                       n_clicks=0,
                       color='dark'),
        ]),
    ], style={'position': 'relative', 'zIndex': 999}),
    html.Br(),
    # DATATABLE
    dbc.Row([
        html.Br(),
        dbc.Col(lg=1),
        dbc.Col([
            DataTable(
                id='fund_table',
                columns=[{'name': i, 'id': i} for i in df.columns],
                # data=pd.DataFrame({k: ['' for i in range(10)] for k in table_columns}).to_dict('rows'),
                data=df.to_dict('records'),
                page_size=15,
                sort_action='native',
                page_action='native',
                # style_table={'overflowX': 'scroll'},
                style_header={
                    'textAlign': 'center',
                    'fontWeight': 'bold'
                },
                style_cell={
                    'font-family': 'Source Sans Pro',
                    'minWidth': 100,
                    'textAlign': 'center'
                },
                style_data={
                    'whiteSpace': 'normal',
                    'height': 'auto'
                },
                style_cell_conditional=[
                    {
                        'if': {'column_id': 'Name'},
                        'textAlign': 'left'
                    },
                    {
                        'if': {'column_id': 'Category'},
                        'textAlign': 'left'
                    }
                ],
            )
        ], lg=10)], style={'font-family': 'Source Sans Pro'}),
]
+ [html.Br() for i in range(8)],
       style = {'background-color': '#eeeeee', 'font-family': 'Source Sans Pro', 'zIndex': 999},
       fluid = True)

#########################
# CALLBACKS
#########################

@ app.callback(Output('fund_table', 'data'),
               [Input('submit_button', 'n_clicks')],
               [State('category_id', 'value'),
                State('activepassive_id', 'value')])
def set_table_data(n_clicks, category_id, activepassive_id):
    if not n_clicks:
        raise PreventUpdate
    filtered_df = df[df['Category'] == category_id]
    filtered_dff = filtered_df[filtered_df['Active-Passive'] == activepassive_id]
    return filtered_dff.to_dict('records')

#########################
# Endzone
#########################

if __name__ == '__main__':
    app.run_server(debug=True)
