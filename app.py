from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

# Sample data
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "NYC", "NYC", "NYC"]
})

# Create Dash app
app = Dash(__name__)
app.layout = html.Div([
    html.H1("Minimal Dash App"),
    dcc.Graph(
        id='example-graph',
        figure=px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")
    )
])

# Expose Flask server for Render
server = app.server

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8080)
