import dash
from dash import Dash, html, dcc, callback, Output, Input, State, ctx
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

from .layouts import create_layout, METRIC_OPTIONS, POPUP_DESC
from .preprocessing import clean_and_convert_types, get_choropleth_data, get_butterfly_data, get_radar_data,  get_stacked_bar_data
from .figures.choropleth import create_choropleth
from .figures.radar import create_radar_chart
from .figures.stacked_bar import create_stacked_bar_chart
from .figures.butterfly import create_butterfly_chart


GOOGLE_FONTS = "https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap"

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP, GOOGLE_FONTS],
    assets_folder="../assets"
)
    
# Load and clean data
df_clean = clean_and_convert_types()

# Generate initial choropleth data for treatment rate
choropleth_df = get_choropleth_data(df_clean, 'treatment_rate')
butterfly_df = get_butterfly_data(df_clean)
stacked_df = get_stacked_bar_data(df_clean)
radar_df = get_radar_data(df_clean)


figures = {
    'choropleth': create_choropleth(choropleth_df, 'treatment_rate'),
    'radar': create_radar_chart(radar_df),
    'stacked_bar': create_stacked_bar_chart(stacked_df),
    'butterfly': create_butterfly_chart(butterfly_df)
}

app.layout = create_layout(figures)

# Callback to update choropleth based on dropdown selection
@callback(
    Output('choropleth', 'figure'),
    Output('sel-metric-store', 'data'),
    Input('metric-dropdown', 'value')
)

def update_choropleth(selected_metric):
    # Get label for the selected metric
    
    # Generate new choropleth data
    choropleth_data = get_choropleth_data(df_clean, selected_metric)
    
    # Create and return the updated figure
    return create_choropleth(choropleth_data, selected_metric), selected_metric

# Callback to display popup on country click
@callback(
    Output("popup", "style"),
    Output("header-text", "children"),
    Output("percentage", "children"),
    Output("metric-desc", "children"),
    Output("temp-click-store", "data"),
    Input("choropleth", "clickData"),
    State("sel-metric-store", "data")
)

def display_popup(clickData, selected_metric):
    if clickData is None:
        return {
                "display": "none",
                }, None, None, None, None
    
    country_name = clickData['points'][0]['customdata'][0]
    percentage = f"{round(clickData['points'][0]['customdata'][1])}%"

    metric_label = next(
        (opt['label'] for opt in POPUP_DESC if opt['value'] == selected_metric),
        selected_metric
    )
    return {
            "top": clickData['points'][0]['bbox']['y0'],
            "left": clickData['points'][0]['bbox']['x0'],
            }, country_name, percentage, metric_label, country_name

# Close popup
@app.callback(
    Output("popup", "style", allow_duplicate=True),
    Input("popup-close", "n_clicks"),
    prevent_initial_call=True
)
def close_popup(clicks):
    return {"display": "none"}

# Save selected country to the appropriate slot
@app.callback(
    Output("selected-ctry1-store", "data", allow_duplicate=True),
    Output("selected-ctry2-store", "data", allow_duplicate=True),
    Output("popup", "style", allow_duplicate=True),
    Input("btn-sel1", "n_clicks"),
    Input("btn-sel2", "n_clicks"),
    State("temp-click-store", "data"),
    prevent_initial_call=True,
)
def save_selection(btn1, btn2, temp_country):
    triggered_id = ctx.triggered_id
    
    # Initialize outputs (keep existing data if not updating that slot)
    out_slot1 = dash.no_update
    out_slot2 = dash.no_update
    
    if triggered_id == "btn-sel1":
        out_slot1 = temp_country
    elif triggered_id == "btn-sel2":
        out_slot2 = temp_country

    return out_slot1, out_slot2, { "display": "none",}

# Update secondary graphs based on selected countries
@app.callback(
    Output("stacked-bar", "figure"),
    Output("butterfly", "figure"),
    Output("radar", "figure"),
    Input("selected-ctry1-store", "data"),
    Input("selected-ctry2-store", "data"),
    prevent_initial_call=True
)
def update_secondary_graphs(country_name1, country_name2):
    # Update stacked bar chart
    stacked_data = get_stacked_bar_data(df_clean, country_name1, country_name2)
    stacked_fig = create_stacked_bar_chart(stacked_data)
    
    # Update butterfly chart
    butterfly_data = get_butterfly_data(df_clean, country_name1, country_name2)
    butterfly_fig = create_butterfly_chart(butterfly_data)
    
    # Update radar chart
    radar_data = get_radar_data(df_clean, country_name1, country_name2)
    radar_fig = create_radar_chart(radar_data)

    return stacked_fig, butterfly_fig, radar_fig

# Update country labels based on selections
@app.callback(
    Output("ctry-1-tag", "children"),
    Output("ctry-1-container", "style", allow_duplicate=True),
    Output("ctry-1-trash", "style", allow_duplicate=True),
    Input("selected-ctry1-store", "data"),
    prevent_initial_call=True
)
def update_label_1(country_name):
    if not country_name:
        return "Empty", {"opacity": 0.2}, {"cursor": "default"}
    return country_name, {"opacity": 1}, {"cursor": "pointer"}

@app.callback(
    Output("ctry-2-tag", "children"),
    Output("ctry-2-container", "style", allow_duplicate=True),
    Output("ctry-2-trash", "style", allow_duplicate=True),
    Input("selected-ctry2-store", "data"),
    prevent_initial_call=True
)
def update_label_2(country_name):
    if not country_name:
        return "Empty", {"opacity": 0.2}, {"cursor": "default"}
    return country_name, {"opacity": 1}, {"cursor": "pointer"}

# Remove selected country 1
@app.callback(
    Output("selected-ctry1-store", "data"),
    Output("ctry-1-container", "style"),
    Output("ctry-1-trash", "style"),
    Input("ctry-1-trash", "n_clicks")
)
def remove_country_1(clicks):
    return None, {"opacity": 0.2}, {"cursor": "default"}

# Remove selected country 2
@app.callback(
    Output("selected-ctry2-store", "data"),
    Output("ctry-2-container", "style"),
    Output("ctry-2-trash", "style"),
    Input("ctry-2-trash", "n_clicks")
)
def remove_country_2(clicks):
    return None, {"opacity": 0.2}, {"cursor": "default"}

# Expose Flask server for Render
server = app.server

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
