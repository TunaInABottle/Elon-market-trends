# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
import dash
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc


app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

predictions = {"Tesla": +0.5, "Bitcoin": -0.3, "Dogecoin": -0.2}
colors = ("green", "darkorange", "blue") # blue for zero maybe?

app.layout = dbc.Container(
    dbc.Row(
        dbc.Col(
            [
            html.Br(),
            html.H2('Elon makes the world go round 💸', className='page-title', style={'text-align': 'center' }),
            html.Br(),
            dbc.Card(
                [
                dbc.CardBody(
                    [
                        html.H2('Latest tweet by Elon Musk', className='card-title'),
                        html.P('and how we predict it will change stocks & crypto', className='card-subtitle'),
                        html.Br(),
                        html.P('This is the most recent Tweet by @ElonMusk. Probably contains lots of arrogance & money 🤑', className='card-text'),
                        html.B('Predictions:', className='card-text'),
                        html.P(f"Tesla: {predictions['Tesla']}" , className='card-text', style={'color': colors[0] if predictions['Tesla'] > 0 else colors[1]}),
                        html.P(f"Bitcoin: {predictions['Bitcoin']}" , className='card-text', style={'color': colors[0] if predictions['Bitcoin'] > 0 else colors[1]}),
                        html.P(f"Dogecoin: {predictions['Dogecoin']}" , className='card-text', style={'color': colors[0] if predictions['Dogecoin'] > 0 else colors[1]}),


                    ]
                )
            ]),
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
        justify='center'
    )
)

if __name__ == '__main__':
    app.run_server(debug=True)
