import plotly.graph_objects as go
from ..theme import COUNTRY_COLORS, CHART_TITLE_STYLE, FONT

def create_radar_chart(radar_data):
    """
    Create a radar chart for mental health metrics.
    
    Args:
        radar_data (dict): Output from get_radar_data()
    
    Returns:
        fig (go.Figure): Plotly radar chart figure
    """

    countries = [radar_data["country1"]]
    if radar_data["country2"]:
        countries.append(radar_data["country2"])
    
    metrics = radar_data['metrics']

    fig = go.Figure()

    for country in countries:
        values = country['values']
        
        fig.add_trace(go.Scatterpolar(
            r = values + [values[0]],
            theta=metrics + [metrics[0]],
            fill=None,
            name=country['name'],
            marker_color=COUNTRY_COLORS['country1'] if country['name'] == countries[0]['name'] else COUNTRY_COLORS['country2'],
            hovertemplate='%{theta}: %{r}%<extra></extra>'
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                autorange=True, 
                rangemode='tozero',
                tickvals=[0, 20, 40, 60, 80, 100],
                ticktext=['0%', '20%', '40%', '60%', '80%', '100%'],
                angle=45,
                tickfont=dict(size=10),
                tickangle=45
            )
        ),
        showlegend=True,
        title=dict(
            text="Comparison of Key Mental Health Indicators",
            **CHART_TITLE_STYLE
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=80, r=30, t=65, b=30),
        font_family=FONT, font_color="black"
    )

    return fig

