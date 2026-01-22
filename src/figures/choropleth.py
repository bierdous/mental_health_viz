import plotly.express as px


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
        color_continuous_scale="Viridis",
        labels={
            "metric_value": "Percentage (%)",
            "respondents": "Respondents"
        },
        title=f"Global Distribution: {metric_label}"
    )
    
    fig.update_layout(
        margin={"r": 0, "t": 50, "l": 0, "b": 0},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='equirectangular',
            bgcolor="rgba(0,0,0,0)"
        )
    )
    
    return fig