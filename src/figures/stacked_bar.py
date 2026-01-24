import plotly.graph_objects as go

def create_stacked_bar_chart():
    categories = ['Metric A', 'Metric B', 'Metric C']

    fig = go.Figure(data=[
        go.Bar(name='Group 1', x=categories, y=[20, 14, 23]),
        go.Bar(name='Group 2', x=categories, y=[12, 18, 29]),
        go.Bar(name='Group 3', x=categories, y=[15, 25, 10])
    ])
    
    fig.update_layout(
        title="Stacked Bar Placeholder",
        barmode='stack',
        margin={"r": 0, "t": 50, "l": 0, "b": 0},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    return fig
