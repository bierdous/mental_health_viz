from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

from .layouts import create_layout
from .preprocessing import clean_and_convert_types, get_choropleth_data
from .figures.choropleth import create_choropleth

app = Dash(
    __name__,
    assets_folder="../assets"
)

# Load and clean data
df_clean = clean_and_convert_types()

# Generate choropleth data for treatment rate
choropleth_df = get_choropleth_data(df_clean, 'treatment_rate')

# Create figures
figures = {
    'choropleth': create_choropleth(choropleth_df, 'Treatment Rate')
}

app.layout = create_layout(figures)

# Expose Flask server for Render
server = app.server

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
