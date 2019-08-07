import plotly.graph_objs as go
import sqlite3
import pandas as pd
import time

from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
from .server import app

conn = sqlite3.connect('./Twitterdata.db')
c = conn.cursor()
df = pd.read_sql("SELECT * FROM sentiment ORDER BY unix", conn)
df.sort_values('unix', inplace=True)

now = time.time()
df["day"] = now - df["unix"]/1000
df.loc[df["day"]<= 86400,"daycount"] = -1
df.loc[(86400 < df["day"]) & (df["day"]<= 172800),"daycount"] = -2
df.loc[(172800 < df["day"]) & (df["day"]<= 259200),"daycount"] = -3
df.loc[(259200 < df["day"]) & (df["day"]<= 345600),"daycount"] = -4
df.loc[(345600 < df["day"]) & (df["day"]<= 432000),"daycount"] = -5
df.loc[(432000 < df["day"]) & (df["day"]<= 518400),"daycount"] = -6
df.loc[df["day"]>518400,"daycount"] = -7



app.layout = html.Div([
    html.Div([
        html.H1("Sentiment in esport")
        ], style={
        'textAlign': "center"
        }),
    dcc.Graph(id='The sentiment of esport game'),
        html.Div([
        html.H2("Select game")
        ], style={
        'textAlign': "left"
        }),
    dcc.Dropdown(
        id='dropdown-game',
        options=[
            {'label': 'MTGA', 'value': 'MTGA'},
            {'label': 'LeagueOfLegends', 'value': 'LeagueOfLegends'},
            {'label': 'Fortnite', 'value': 'Fortnite'},
            {'label': 'ApexLegends', 'value': 'ApexLegends'},
            {'label': 'SSBU', 'value': 'SSBU'},
            {'label': 'dota2', 'value': 'dota2'},
            {'label': 'Hearthstone', 'value': 'Hearthstone'},
            {'label': 'Overwatch', 'value': 'Overwatch'},
            {'label': 'PUBG', 'value': 'PUBG'}
        ],
        value=["MTGA","LeagueOfLegends","Fortnite","ApexLegends","SSBU","dota2","Hearthstone","Overwatch","PUBG"],
        multi = True
    ),
    html.Div([
        html.H2("Select language")
        ], style={
        'textAlign': "left"
        }),
    dcc.Dropdown(
        id='my-dropdown',
        options=[
            {'label': 'english', 'value': 'en'},
            {'label': 'french', 'value': 'fr'}
        ],
        value=['en','fr'],
        multi = True
    ),
    html.Div([
        html.H2("Select day")
        ], style={
        'textAlign': "left"
        }),
    dcc.Slider(
        id='day-slider',
        min= -7,
        max= -1,
        value= -7,
        marks={day: nameday for (day,nameday) in [(-7,"Seven days ago"),(-6,"Six days ago"),(-5,"Five days ago"),
        (-4,"Four days ago"),(-3,"Three days ago"),(-2,"Two days ago"),(-1,"One day ago")]},
        step=None
    ),
])

@app.callback(
    Output('The sentiment of esport game', 'figure'),
    [Input('day-slider', 'value'),
    Input('dropdown-game','value'),
    Input('my-dropdown','value')])

def update_figure(selected_day,selected_trackword,selected_lang):
    filtered_df = df[df.daycount == selected_day]
    filtered_df = filtered_df[filtered_df.trackword.isin(selected_trackword)]
    filtered_df = filtered_df[filtered_df.lang.isin(selected_lang)]
    mean = filtered_df.groupby(["trackword"]).mean().sort_index()
    frequency = pd.value_counts(filtered_df["trackword"]).to_frame().sort_index()
    data = pd.concat([mean,frequency],axis=1)
    data["trackword"] = data["trackword"]/data["trackword"].sum()

    return {
    'data': [
    go.Scatter(
        x=data["trackword"],
        y=data["sentiment"],
        mode='markers+text',
        opacity=0.8,
        text = data.index.values,
        textposition='top center',
        marker={'size': 15,
        "color": "orange",
        "opacity": 0.8,
        "line": {"color": "#4C5050", "width": 0.5}
        },
        ) 
    ],
    'layout': go.Layout(
        xaxis=go.layout.XAxis(
            title=go.layout.xaxis.Title(
                text='Proportion of tweets',
                font=dict(
                    family='Courier New, monospace',
                    size=18,
                    color='#7f7f7f'
                    )
                )
            ),
        yaxis=go.layout.YAxis(
            title=go.layout.yaxis.Title(
                text='sentiment',
                font=dict(
                    family='Courier New, monospace',
                    size=18,
                    color='#7f7f7f'
                    )
                )
            ),
        margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
        legend={'x': 0, 'y': 1}
        )
    }

if __name__ == '__main__':
    app.run_server(debug=True)