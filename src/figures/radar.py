import plotly.graph_objects as go

def create_radar_chart(radar_data):
    """
    Create a radar chart for mental health metrics.
    
    Args:
        radar_data (dict): Output from get_radar_data()
    
    Returns:
        fig (go.Figure): Plotly radar chart figure
    """
    metrics = radar_data['metrics']
    
    fig = go.Figure()
    
    # Country 1
    values1 = radar_data['country1']['values']

    fig.add_trace(go.Scatterpolar(
        r=values1 + [values1[0]],
        theta=metrics + [metrics[0]],
        fill='toself',
        name=radar_data['country1']['name'],
        marker_color='#1f77b4',
        hovertemplate='%{theta}: %{r}%<extra></extra>'
    ))
    
    # Country 2 if exists
    if radar_data.get('country2'):
        values2 = radar_data['country2']['values']

        fig.add_trace(go.Scatterpolar(
            r=values2 + [values2[0]],
            theta=metrics + [metrics[0]],
            fill='toself',
            name=radar_data['country2']['name'],
            marker_color='#ff7f0e',
            hovertemplate='%{theta}: %{r}%<extra></extra>'
        ))
    
    # Layout
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
        title="Mental Health Radar Chart",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=80, r=20, t=60, b=30),
        font_family="Roboto", font_color="black"
    )
    
    return fig
