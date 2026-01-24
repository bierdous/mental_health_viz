import plotly.graph_objects as go

def create_radar_chart():
    categories = ['Mental Health', 'Physical Health', 'Social', 'Work', 'Family']

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=[4, 3, 2, 5, 4],
        theta=categories,
        fill='toself',
        name='Group A'
    ))

    fig.update_layout(
        title="Radar Chart Placeholder",
        margin={"r": 40, "t": 50, "l": 40, "b": 20},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5]
            )
        ),
        showlegend=False
    )
    return fig
