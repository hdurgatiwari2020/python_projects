import requests

import json

import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
#import random
import plotly.graph_objs as go
from collections import deque



def by_three(number):
    return number**3 if number % 3 == 0 else False

def get_json(url):
    return requests.get(url)

url_val = 'https://script.google.com/macros/s/AKfycbyaPf7m4DjWffO9Fpfywt9QCT8lVcJdaJFv3si4zJ_uqKw3h5b2/exec'

x = get_json(url_val)

loaded_json = json.loads(x.text)

print(x.text)

print(loaded_json[0]["Timestamp"])

print(by_three(7))

#x = requests.get('https://script.google.com/macros/s/AKfycbyaPf7m4DjWffO9Fpfywt9QCT8lVcJdaJFv3si4zJ_uqKw3h5b2/exec')

#var url_val = 'https://script.google.com/macros/s/AKfycbyaPf7m4DjWffO9Fpfywt9QCT8lVcJdaJFv3si4zJ_uqKw3h5b2/exec'

#x = get_json('https://script.google.com/macros/s/AKfycbyaPf7m4DjWffO9Fpfywt9QCT8lVcJdaJFv3si4zJ_uqKw3h5b2/exec')

X = deque(maxlen = 20) 
X.append(loaded_json[0]["Timestamp"]) 
  
Y = deque(maxlen = 20) 
Y.append(loaded_json[0]["Data"]) 
  
app = dash.Dash(__name__) 
  
app.layout = html.Div( 
    [ 
        dcc.Graph(id = 'live-graph', animate = True), 
        dcc.Interval( 
            id = 'graph-update', 
            interval = 1000, 
            n_intervals = 0
        ), 
    ] 
) 
  
@app.callback( 
    Output('live-graph', 'figure'), 
    [ Input('graph-update', 'n_intervals') ] 
) 
  
def update_graph_scatter(n): 
    X.append(loaded_json[0]["Timestamp"]) 
    Y.append(loaded_json[0]["Data"]) 
    print(X)
    print(Y)
  
    data = plotly.graph_objs.Scatter( 
            x=list(X), 
            y=list(Y), 
            name='Scatter', 
            mode= 'lines+markers'
    ) 
  
    return {'data': [data], 
            'layout' : go.Layout(xaxis=dict(range=[min(X),max(X)]),yaxis = dict(range = [min(Y),max(Y)]),)} 
  
if __name__ == '__main__': 
    app.run_server()