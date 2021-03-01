import dash
import dash_core_components as dcc
import dash_html_components as html
# import html as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
import pandas as pd
from os import listdir, remove
import pickle
from time import sleep
from helper_functions import *  # this statement imports all functions from your helper_functions file!

# Run your helper function to clear out any io files left over from old runs
# 1:
check_for_and_del_io_files()

# Make a Dash app!
app = dash.Dash(__name__)

# Define the layout.
app.layout = html.Div([

    # Section title
    html.H1("Section 1: Fetch & Display exchange rate historical data"),

    # Currency pair text input, within its own div.
    html.Div(
        [
            "Input Currency: ",
            # Your text input object goes here:
            dcc.Input(id='currency-pair', type='text'),
        ],

        # Style it so that the submit button appears beside the input.
        style={'display': 'inline-block'}
    ),

    # Submit button:
    html.Button('Submit', id='submit-button', n_clicks=0),

    # Line break
    html.Br(),

    # Div to hold the initial instructions and the updated info once submit is pressed
    html.Div(id='output-currency', children='Enter a currency code and press \'Submit\''),

    html.Div([
        # Candlestick graph goes here:
        dcc.Graph(id='candlestick-graph')
    ]),

    # Another line break
    html.Br(),

    # Section title
    html.H1("Section 2: Make a Trade"),

    # Div to confirm what trade was made
    html.Div(id='output-trade'),

    # Radio items to select buy or sell
    html.Div([
        dcc.RadioItems(
            id='trade-option',
            options=[
                {'label': 'BUY', 'value': 'BUY'},
                {'label': 'SELL', 'value': 'SELL'},
            ],
            value='BUY',
            labelStyle={'display': 'inline-block'}
        )
    ]),

    # Text input for the currency pair to be traded
    html.Div(
        [
            "Trade Currency: ",
            # Your text input object goes here:
            dcc.Input(id='trade-pair', type='text'),
        ],
    ),

    # Numeric input for the trade amount
    html.Div(
        [
            "Trade Amount: ",
            # Your text input object goes here:
            dcc.Input(id='trade-amount', type='number'),
        ],

        # Style it so that the submit button appears beside the input.
        style={'display': 'inline-block'}
    ),

    # Submit button for the trade
    html.Button('Trade', id='trade-button', n_clicks=0)
])

@app.callback(
    [dash.dependencies.Output('output-currency', 'children'),
     dash.dependencies.Output('candlestick-graph', 'figure')],
    [dash.dependencies.Input('submit-button', 'n_clicks')],
    [dash.dependencies.State('currency-pair', 'value')],
    prevent_initial_call=True
)
def update_candlestick_graph(n_clicks, value):
    # if n_clicks == 0:
    #     return 'Enter a currency code and press \'Submit\'', go.Figure()
    # Now we're going to save the value of currency-input as a text file.
    f = open("currency_pair.txt", "w")
    f.write(value)
    f.close()

    # Wait until ibkr_app runs the query and saves the historical prices csv
    while "currency_pair_history.csv" not in listdir():
        sleep(.01)

    # Read in the historical prices
    df = pd.read_csv("currency_pair_history.csv")

    # Remove the file 'currency_pair_history.csv'
    remove("currency_pair_history.csv")

    # Make the candlestick figure
    fig = go.Figure(
        data=[
            go.Candlestick(
                x=df['date'],
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close']
            )
        ]
    )
    # Give the candlestick figure a title
    fig.update_layout(title= value + ' OHLC')

    # Return your updated text to currency-output, and the figure to candlestick-graph outputs
    return ('Submitted query for ' + value), fig

# Callback for what to do when trade-button is pressed
@app.callback(
    dash.dependencies.Output('output-trade', 'children'),
    [dash.dependencies.Input('trade-button', 'n_clicks')],
    [dash.dependencies.State('trade-option', 'value'),
     dash.dependencies.State('trade-pair', 'value'),
     dash.dependencies.State('trade-amount', 'value')],
    # We DON'T want to start executing trades just because n_clicks was initialized to 0!!!
    prevent_initial_call=True
)
def trade(n_clicks, action, trade_currency, trade_amt): # Still don't use n_clicks, but we need the dependency

    # Make the message that we want to send back to trade-output
    msg = "Trade: " + action + " " + str(trade_amt) + " "  + trade_currency

    # Make our trade_order object -- a DICTIONARY.
    dic = {
        "action": action,
        "trade_currency": trade_currency,
        "trade_amt": trade_amt
    }
    # Dump trade_order as a pickle object to a file connection opened with write-in-binary ("wb") permission:
    pickle.dump(dic, open("trade_order.p", "wb"))

    # Return the message, which goes to the trade-output div's "children" attribute.
    return msg


# Run it!
if __name__ == '__main__':
    app.run_server(debug=True)
