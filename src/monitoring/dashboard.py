# src/monitoring/dashboard.py
import dash
from dash import dcc, html
import plotly.graph_objs as go
from src.data.storage import DatabaseClient

# Initialize Dash app
app = dash.Dash(__name__)

def serve_dashboard():
    db = DatabaseClient()
    data = db.load_ohlcv("BTC/USDT", limit=1000)

    # Price chart
    price_chart = dcc.Graph(
        id='price-chart',
        figure={
            'data': [go.Scatter(x=data['timestamp'], y=data['close'], name='BTC/USDT')],
            'layout': go.Layout(title='Price History')
        }
    )

    # Portfolio metrics
    metrics = html.Div([
        html.H3("Portfolio Performance"),
        html.P(f"Total Trades: {len(data)}"),
        html.P(f"Current Balance: $10,000")  # Example
    ])

    app.layout = html.Div([price_chart, metrics])
    return app

if __name__ == "__main__":
    app = serve_dashboard()
    app.run_server(debug=True)