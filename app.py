# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
import dash
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import model_one
from kafkaCustomProducer import last_message_in_topic, TopicPartition
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

last_tweet = last_message_in_topic(TopicPartition("TWEETS", 0))
print(last_tweet)
print("New tweet! Computing prediction...")
predictions = model_one.predict()
print(predictions)

colors = ("green", "darkorange", "blue") # green for positive, red for negative, blue for neutral

app.layout = dbc.Container(
    dbc.Row(
        dbc.Col(
            [
            html.Br(),
            html.Br(),
            dbc.Card(
                [
                dbc.CardBody(
                    [
                        html.H2('Latest tweet by Elon Musk', className='card-title'),
                        html.P('and how we predict it will change stocks & crypto', className='card-subtitle'),
                        html.Br(),
                        dbc.Card(
                            dbc.CardBody([
                                html.P(last_tweet['text'], className='card-text', style={'font-family': 'Helvetica Neue', 'font-size': '18px', 'line-height': '20px' }),
                                html.P(last_tweet['datetime'], className='card-text', style={'font-family': 'Helvetica Neue', 'font-size': '14px', 'font-color': 'grey' }),
                            ]
                        )),
                        html.Br(),
                        html.H3('Predictions:', className='card-title'),
                        html.P(f"Tesla: {predictions['stock_tsla']}" , className='card-text', style={'color': colors[0] if predictions['stock_tsla'] > 0 else colors[1] if predictions['stock_tsla'] < 0 else colors[2]}),
                        html.P(f"Bitcoin: {predictions['crypto_btc']}" , className='card-text', style={'color': colors[0] if predictions['crypto_btc'] > 0 else colors[1] if predictions['crypto_btc'] < 0 else colors[2]}),
                        html.P(f"Dogecoin: {predictions['crypto_doge']}" , className='card-text', style={'color': colors[0] if predictions['crypto_doge'] > 0 else colors[1] if predictions['crypto_doge'] < 0 else colors[2]}),


                    ]
                )
            ], style= {'backgroundColor':'#f5f5f5'}), 
            html.Br(),
            dbc.Card(
                [
                dbc.CardBody(
                    [
                        html.H2('What if you could influence markets? (optional if easy)', className='card-title'),
                        html.P('Our predictions if your text would be a Tweet by Elon Musk', className='card-subtitle'),
                        html.Br(),
                        html.Textarea('I WANT TO BUY MORE BITCOIN cause im richer than you loosers 🤑', className='card-textarea'),
                        html.Br(),
                        dbc.Button("Predict", color="primary"),
                    ]
                )
            ])
        ]),
        justify='center',
    ),
)

if __name__ == '__main__':
    app.run_server(debug=True)

