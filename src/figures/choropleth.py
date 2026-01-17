import plotly.express as px

def create_choropleth(df, indicator):
    fig = px.choropleth(
        df,
        locations="Country",
        locationmode="country names",
        color=indicator,
        color_continuous_scale="Viridis",
        title=f"Global distribution of {indicator}"
    )
    return fig