from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

from .layouts import create_layout, METRIC_OPTIONS
from .preprocessing import clean_and_convert_types, get_choropleth_data
from .figures.choropleth import create_choropleth
from .figures.radar import create_radar_chart
from .figures.stacked_bar import create_stacked_bar_chart
from .figures.butterfly import create_butterfly_chart

app = Dash(
    __name__,
    assets_folder="../assets"
)

#df = pd.read_csv("data/processed/mental_health_clean.csv")

figures = {
    'choropleth': create_choropleth(choropleth_df, 'Treatment Rate'),
    'radar': create_radar_chart(),
    'stacked_bar': create_stacked_bar_chart(),
    'butterfly': create_butterfly_chart()
}

app.layout = create_layout()

# Expose Flask server for Render
server = app.server

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
