import plotly.graph_objects as go

def create_butterfly_chart():
    y_categories = ['Age 18-25', 'Age 26-35', 'Age 36-45', 'Age 46+']
    x_male = [15, 25, 20, 10]
    x_female = [18, 28, 22, 12]
    
    # Negate one side for the butterfly effect
    x_male_neg = [-x for x in x_male]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=y_categories,
        x=x_male_neg,
        name='Male',
        orientation='h',
        customdata=x_male,
        hovertemplate='%{y}: %{customdata}'
    ))
    
    fig.add_trace(go.Bar(
        y=y_categories,
        x=x_female,
        name='Female',
        orientation='h',
        hovertemplate='%{y}: %{x}'
    ))
    
    fig.update_layout(
        title="Butterfly Chart Placeholder",
        barmode='relative',
        margin={"r": 0, "t": 50, "l": 0, "b": 0},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(
            title="Count",
            tickmode='array',
            tickvals=[-30, -20, -10, 0, 10, 20, 30],
            ticktext=[30, 20, 10, 0, 10, 20, 30]
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    return fig
