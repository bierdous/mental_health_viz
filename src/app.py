from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

from .layouts import create_layout, METRIC_OPTIONS
from .preprocessing import clean_and_convert_types, get_choropleth_data
from .figures.choropleth import create_choropleth

app = Dash(
    __name__,
    assets_folder="../assets"
)

# Load and clean data
df_clean = clean_and_convert_types()

# Generate initial choropleth data for treatment rate
choropleth_df = get_choropleth_data(df_clean, 'treatment_rate')

# Create initial figures
figures = {
    'choropleth': create_choropleth(choropleth_df, 'Treatment Rate')
}

app.layout = create_layout(figures)


# Callback to update choropleth based on dropdown selection
@callback(
    Output('choropleth', 'figure'),
    Input('metric-dropdown', 'value')
)

def update_choropleth(selected_metric):
    # Get label for the selected metric
    metric_label = next(
        (opt['label'] for opt in METRIC_OPTIONS if opt['value'] == selected_metric),
        selected_metric
    )
    
    # Generate new choropleth data
    choropleth_data = get_choropleth_data(df_clean, selected_metric)
    
    # Create and return the updated figure
    return create_choropleth(choropleth_data, metric_label)


# Expose Flask server for Render
server = app.server

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
