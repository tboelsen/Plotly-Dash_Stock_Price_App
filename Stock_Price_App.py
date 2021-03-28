import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import pandas_datareader.data as web
import pandas_datareader.nasdaq_trader as nsdq
from datetime import datetime, timedelta

api_key = 'Your_API_KEY'

# Step 1 - Import the data
tickers = nsdq.get_nasdaq_symbols()
keep = ['Security Name', 'ETF']
tickers = tickers[keep]

# Step 2 - Launch the application
app = dash.Dash()

# Step 3 - Create a plotly figure
#options for dropdown
options = []
for tic in tickers.index:
    options.append({'label' : '{} {}'.format(tic, tickers.loc[tic]['Security Name']), 'value' : tic})

#for default graph
start = datetime(2018,1,1)
end = datetime.today()
cvx = web.DataReader('CVX', 'av-daily-adjusted', start, end, api_key = api_key)
trace_1 = go.Scatter(x = cvx.index, y = cvx['adjusted close'], mode = 'lines',
                    name = 'CVX')
layout = go.Layout(title = 'CVX Adj. Close Price [USD]',
                   hovermode = 'closest')
figure = go.Figure(data = [trace_1], layout = layout)

# Step 4 - Create a Dash layout
app.layout = html.Div([
                    html.Div([
                    html.H1('Stock Ticker Dashboard'),
                            ], style = {'margin' : 25, 'textAlign' : 'center', 'border' : 'solid', 'backgroundColor' : 'silver'}),
                html.Div([
                    html.Div([
                            html.H3(' Select stock symbols: '),
                            dcc.Dropdown(
                                        id='symbol',
                                        options=options,
                                        value=['CVX'],
                                        multi=True
                                        )
                            ], style={'display':'inline-block', 'verticalAlign':'top', 'width':'20%' }),
                    html.Div([
                            html.H3('Select start and end dates:'),
                            dcc.DatePickerRange(
                                                id='date_picker',
                                                min_date_allowed=datetime(2000, 1, 1),
                                                max_date_allowed=datetime.today(),
                                                start_date=datetime(2018, 1, 1),
                                                end_date=datetime.today()
                                                )
                            ], style={'display':'inline-block', 'marginLeft':'30px'}),
                    html.Div([
                            html.Button(
                                        id='button',
                                        n_clicks=0,
                                        children='Submit',
                                        style={'fontSize':24, 'marginLeft':'30px'}
                                        ),
                            ], style={'display':'inline-block'}),
                    dcc.Graph(
                                id='graph',
                                figure=figure
                            )
                        ], style = {'margin' : 25})
])

# Step 5 - Add callback functions
@app.callback(
            Output('graph', 'figure'),
            [Input('button', 'n_clicks')],
            [State('symbol', 'value'),
            State('date_picker', 'start_date'),
            State('date_picker', 'end_date')])
def update_graph(n_clicks, stock_ticker, start_date, end_date):
    traces = []
    for tic in stock_ticker:
        df = web.DataReader(tic, 'av-daily-adjusted', start_date, end_date, api_key = api_key)
        traces.append(go.Scatter(x = df.index, y = df['adjusted close'], mode = 'lines',
                            name = tic))
    layout = go.Layout(title = ', '.join(stock_ticker)+' Adj. Close Price [USD]',
                           hovermode = 'closest')
    fig = go.Figure(data = traces, layout = layout)
    return fig

# Step 6 - Add the server clause
if __name__ == '__main__':
    app.run_server()
