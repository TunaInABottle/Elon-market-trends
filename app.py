# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
import dash
from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import model_one
from time import sleep
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

sleep(30)

colors = ("green", "orangeRed", "blue") # colorcoded: green for positive, red for negative, blue for neutral

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
                        html.H2("The impact of Elon Musk's Tweets", className='card-title'),
                        html.P('How we predict they will change market prices & cryptocurrency', className='card-subtitle'),
                        html.P('This is a simple model that predicts the variation of the market prices based on the last tweet of Elon Musk:', className='card-text'),
                        html.Br(),
                        dbc.Card(
                            dbc.CardBody([
                                html.P(last_tweet['text'], className='card-text', style={'font-family': 'Helvetica Neue', 'font-size': '18px', 'line-height': '20px' }),
                                html.P(last_tweet['datetime'], className='card-text', style={'font-family': 'Helvetica Neue', 'font-size': '14px', 'font-color': 'grey' }),
                            ]
                        )),
                        html.Br(),
                        html.H3('Predictions:', className='card-title'),
                        html.P(f"Tesla: {round(predictions['stock_tsla'],3)}" , className='card-text', style={'color': colors[0] if predictions['stock_tsla'] > 0 else colors[1] if predictions['stock_tsla'] < 0 else colors[2]}),
                        html.P(f"Bitcoin: {round(predictions['crypto_btc'],3)}" , className='card-text', style={'color': colors[0] if predictions['crypto_btc'] > 0 else colors[1] if predictions['crypto_btc'] < 0 else colors[2]}),
                        html.P(f"Dogecoin: {round(predictions['crypto_doge'], 3)}" , className='card-text', style={'color': colors[0] if predictions['crypto_doge'] > 0 else colors[1] if predictions['crypto_doge'] < 0 else colors[2]}),


                    ]
                )
            ], style= {'backgroundColor':'#f5f5f5'}), 
            html.Br(),
            dbc.Card(
                [
                dbc.CardBody(
                    [
                        html.H2('What if you were Elon Musk?', className='card-title'),
                        html.P('How would you use Twitter if one of your Tweets could change financial markets? \n Have a look at the predicted changes in stock markets if your text were tweeted by Elon Musk today.', 
                        className='card-subtitle'),
                        html.Br(),
                        dcc.Textarea(id='faketweet', value='Type your influential tweet here\nand push the button', style={'width': '70%', 'height': 100},),
                        html.Br(),
                        dbc.Button("Predict", color="primary", id='faketweet-button', n_clicks=0),
                        html.Br(),
                        html.Div(id='output', style={'whiteSpace': 'pre-line'})
                    ]
                )
            ], style= {'backgroundColor':'#f5f5f5'}),
        ]),
        justify='center',
    ),
)

@app.callback(
    Output('output', 'children'),
    Input('faketweet-button', 'n_clicks'),
    State('faketweet', 'value')
)
def predict_fake_tweet(n_clicks, faketweet):
    if n_clicks > 0:
        print(f"Fake tweet! Computing prediction...")
        fake_predictions = model_one.fake_predict(faketweet)
        print(fake_predictions)
        return(f"Tesla: {round(fake_predictions['stock_tsla'],3)}, Bitcoin: {round(fake_predictions['crypto_btc'],3)}, Dogecoin: {round(predictions['crypto_doge'], 3)}")

if __name__ == '__main__':
    app.run_server(debug=True)
    last_tweet = last_message_in_topic(TopicPartition("TWEETS", 0))
    sleep_time = 30 * 60 # 30 minutes
    while True:
        print("model_one: Model ready to execute")
        if last_tweet != last_message_in_topic(TopicPartition("TWEETS", 0)):
            print("New tweet! Computing prediction...")
            predictions = model_one.predict()
            print(predictions)
            last_tweet = last_message_in_topic(TopicPartition("TWEETS", 0))
        else:
            print("model_one: No new tweet detected")
        print(f"Returning to sleep for {sleep_time} seconds")
        predictions = predictions = {"crypto_btc": 0, "crypto_doge": 0, "stock_tsla": 0}
        sleep( sleep_time )

