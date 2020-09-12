
import dash
import datetime
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from numpy import random
import numpy as np
import random
import time
import sqlite3
import re
import pandas as pd
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


app = dash.Dash(external_stylesheets=external_stylesheets)

colors = {
    'background': '#111111',
    'text': '#FFFFFF'
}

def scatterfun():
    conn = sqlite3.connect('OregonFiretwitter.db')
    c = conn.cursor()

    df = pd.read_sql("SELECT * FROM oregontweetanalysis ORDER BY created_at DESC LIMIT 1000", conn)
    df.dropna()
    sentimentcount=df.groupby("sentiment").count()["id_str"]
    df["created_at"]=pd.to_datetime(df["created_at"])
    df2 = pd.get_dummies(df["sentiment"])
    df.reset_index(drop=True, inplace=True)
    df2.reset_index(drop=True, inplace=True)
    df=pd.concat([df, df2], axis=1)
    df = df.set_index(['created_at'])
    df=df.replace({0:np.nan})
    k=df.groupby(pd.TimeGrouper(freq='15Min')).count().index
    k=k.tolist()

    for i in k:
        i=str(i)
        i=i.replace('Timestamp(','')
      
        i=i.replace(", freq='15T')","")

    neutral=df.groupby(pd.TimeGrouper(freq='15Min')).count()["Neutral"]
    neutral.tolist()

    negative=df.groupby(pd.TimeGrouper(freq='15Min')).count()["Negative"]
    negative.tolist()

    positive=df.groupby(pd.TimeGrouper(freq='15Min')).count()["Positive"]
    positive.tolist()

    trace1=go.Scatter(x=k, y=negative, mode = 'lines+markers',name='Negative')
    trace2=go.Scatter(x=k, y=neutral, mode = 'lines+markers',name='Neutral')
    trace3=go.Scatter(x=k, y=positive, mode = 'lines+markers',name='Positive')

    return trace1,trace2,trace3


def topictrack():
    conn = sqlite3.connect('OregonFiretwitter.db')
    c = conn.cursor()
    df = pd.read_sql("SELECT * FROM oregontweetanalysis ORDER BY created_at DESC LIMIT 1000", conn)
    df.dropna()
    content = ' '.join(df["tweet"])
    content = re.sub(r"http\S+", "", content)
    content = content.replace('RT ', ' ').replace('&amp;', 'and')
    content = re.sub('[^A-Za-z0-9]+', ' ', content)
    content = content.lower()

    tokenized_word = word_tokenize(content)
    stop_words=set(stopwords.words("english"))
    filtered_sent=[]
    for w in tokenized_word:
        if w not in stop_words:
            filtered_sent.append(w)
    fdist = FreqDist(filtered_sent)
    fd = pd.DataFrame(fdist.most_common(10),                 
    columns = ["Word","Frequency"]).drop([0]).reindex()

    fd=fd.values.tolist()
    topics=[]
    val=[]
    for i in fd:
        topics.append(i[0])
        val.append(i[1])
    return topics,val


topics,val=topictrack()

def tweetmentions():
    conn = sqlite3.connect('OregonFiretwitter.db')
    c = conn.cursor()
    a=c.execute("Select count(*) from oregontweetanalysis;")
    conn.commit()
    k=str(a.fetchall())
    mentions=int(re.sub('\D', '',k))
    return mentions

trace1,trace2,trace3=scatterfun()
mentions=tweetmentions()

def sentimentcount():
    conn = sqlite3.connect('OregonFiretwitter.db')
    c = conn.cursor()
    n=c.execute("Select count(*) from oregontweetanalysis  where sentiment='Neutral';")
    conn.commit()
    n=str(n.fetchall())
    neutral=int(re.sub('\D', '',n))

    p=c.execute("Select count(*) from oregontweetanalysis  where sentiment='Positive';")
    conn.commit()
    p=str(p.fetchall())
    positive=int(re.sub('\D', '',p))


    ne=c.execute("Select count(*) from oregontweetanalysis  where sentiment='Negative';")
    conn.commit()
    ne=str(ne.fetchall())
    negative=int(re.sub('\D', '',ne))


    return neutral,positive, negative

neutral,positive, negative=sentimentcount()



app.layout = html.Div(html.Div([
    html.H1(children='Oregon Wildfires tweets Analysis Dashboard',style={'color':'white'}),
    html.Div(children='''Real Time Updates Every Minute''',style={'color':'white'}), 
    dcc.Graph(
        id='graphone', figure={
            'data': [trace1,trace2,trace3],
            'layout': {
                'title': 'Sentiment Analysis (Real-Time Updates)'
            }
        } 
    ), html.H1(children='Total Mentions',style={'text-align': 'center','color':'white'}), html.H1(id='live count',children=mentions,style={'text-align': 'center','color':'white'}),

    dcc.Graph(
        id='graphtwo', figure={
            'data': [
                go.Bar(x=topics, y=val)
            ],
            'layout': {
                'title': 'Live Topics Tracker'
            }
        }
    ), html.H1(children='hi',style={'text-align': 'center','color':'black'}),html.H1(children='chelsea here',style={'text-align': 'center','color':'black'}),
    dcc.Graph(
        id='graphthree', figure={ 'data':[
            go.Pie(labels=['Negative','Positive','Neutral'], values=[negative,positive,neutral], hole=.6)
            ],
            'layout': {
                'title': 'Live Sentiment Aggregation'
            }
        }
    ),
    dcc.Interval(
        id='1-second-interval',
        interval=2000, # 2000 milliseconds = 2 seconds
        n_intervals=0
    ), 
]), style={'background-color':'black'}
)

@app.callback(Output('graphone', 'figure'),
            [Input('1-second-interval', 'n_intervals')])
def update_graphone(n):
    trace1,trace2,trace3=scatterfun()
    figure={
            'data': [trace1,trace2,trace3],
            'layout': {
                'title': 'Sentiment Analysis (Real-Time Updates)'
            }
        }
    return figure



@app.callback(Output('graphtwo', 'figure'),
            [Input('1-second-interval', 'n_intervals')])
def update_graphtwo(n):
    topics,val=topictrack()
    figure={
            'data': [
                go.Bar(x=topics, y=val)
            ],
            'layout': {
                'title': 'Live Topics Tracker'
            }
        }
    return figure        

@app.callback(Output('live count', 'children'),
            [Input('1-second-interval', 'n_intervals')])
def update_live_count(n):
    mention=tweetmentions()
    children=mention
    return children

@app.callback(Output('graphthree', 'figure'),
            [Input('1-second-interval', 'n_intervals')])
def update_graphthree(n):
    neutral,positive, negative=sentimentcount()
    figure={
            'data': [
               go.Pie(labels=['Negative','Positive','Neutral'], values=[negative,positive,neutral], hole=.6)
            ],
            'layout': {
                'title': 'Live Sentiment Aggregation'
            }
        }

    return figure
if __name__ == '__main__':
    
    app.run_server(debug=True)
