import plotly.express as px


"""
Custom titles for choropleth maps based on the selected metric.
"""

def create_choropleth(df, metric_label):
    """
    Create a choropleth map visualization.
    
    Args:
        df (pd.DataFrame): Dataframe returned by get_choropleth_data
                          Columns: [Country, metric_value, respondents]
        metric_label (str): Label for the metric to display in title/legend
    
    Returns:
        plotly.graph_objects.Figure: Choropleth map figure
    """
    fig = px.choropleth(
        df,
        locations="Country",
        locationmode="country names",
        color="metric_value",
        hover_name="Country",
        hover_data={
            "Country": False,
            "metric_value": ":.2f",
            "respondents": True
        },
        color_continuous_scale="YlGnBu",
        labels={
            "metric_value": "Share of Respondents (%)",
            "respondents": "Number of Respondents"
        },
        #title=CHOROPLETH_TITLES[metric_label]
    )
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='equirectangular',
            domain=dict(x=[0.3, 1.0], y=[0, 1.0]),
            bgcolor="rgba(0,0,0,0)"
        ),  
        font_family="Roboto",
        font_color="black",

        # 1. MAXIMIZE THE MAP AREA
        # Setting margins to 0 forces the map to touch the edges of the Div
        margin=dict(l=0, r=0, t=10, b=10),
        
        # Optional: If you want the map to zoom automatically to fit the countries you have
        # geo=dict(fitbounds="locations", visible=False), 

        # 2. SHRINK AND POSITION THE LEGEND (Colorbar)
        coloraxis_colorbar=dict(
        # Size
        len=0.6,          # Height: 0.4 means 40% of the screen height
        thickness=40,     # Width: 10 pixels thin
        
        # Position (Floating inside the map)
        xanchor="right",  # Anchor to the right side
        x=0.21,           # 0.98 means "2% away from the right edge"
        yanchor="bottom", # Anchor to the bottom
        y=0.05,           # 5% up from the bottom edge
        )
    )
    fig.update_traces(hoverinfo='none', hovertemplate=None)
    return fig