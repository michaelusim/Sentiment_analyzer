import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import sqlite3

app = dash.Dash(__name__)

app.layout = html.Div([html.H2("Live Sentiment Graph"), dcc.Graph(id="live-graph", animate=True),
                       dcc.Interval(id="graph-interval", interval=1*1000),
                       dcc.Input(id="sentiment_term", value="donald trump", type="text")])


@app.callback(dash.dependencies.Output("live-graph", "figure"),
              [dash.dependencies.Input(component_id="sentiment_term", component_property="value")],
              events=[dash.dependencies.Event("graph-interval", "interval")])
def get_x_graph(sentiment_term):
    conn = sqlite3.connect("twitter_lite.db")
    df = df = pd.read_sql("SELECT * FROM sentiment WHERE tweet LIKE ? ORDER BY unix DESC LIMIT 1000", conn, params=('%' + sentiment_term + '%',))
    df["sentiment_sample"] = df["sentiment"].rolling(int(len(df)/5)).mean()
    df.dropna(inplace=True)

    X = df.unix[-100:]
    Y= df.sentiment[-100:]
    data = go.Scatter(x=X, y=Y, name='Scatter', mode='lines+markers')
    return {"data": [data], "layout": go.Layout(xaxis=dict(range=[min(X), max(X)]), yaxis=dict(range=[min(Y), max(Y)],))}


if __name__ == '__main__':
    app.run_server(debug=True)
#$ ps ax | grep python  -Kill the Process  -$ kill PROCESS_NAME

    
















