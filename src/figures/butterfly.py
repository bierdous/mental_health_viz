import plotly.graph_objects as go

def create_butterfly_chart(butterfly_data, country2=None):

    countries = [butterfly_data["country1"]]
    if butterfly_data["country2"]:
        countries.append(butterfly_data["country2"])

    days = butterfly_data['days_indoors_order']

    fig = go.Figure()

    for status in ['employed', 'self_employed']:
        for country in countries:
            data = [
                country[status][d]
                for d in days
            ]

            if status == 'employed':
                displayed_data = [-v for v in data]
            else:
                displayed_data = data

            fig.add_trace(go.Bar(
                y=days,
                x=displayed_data,
                orientation='h',
                customdata=data,
                legendgroup=country['name'],
                name=country['name'],
                marker_color="#1f77b4" if country['name'] == countries[0]['name'] else "#d62728",
                hovertemplate='%{y}: %{customdata}',
                showlegend=True if len(countries) > 1 and status == 'employed' else False
            ))

    fig.update_layout(
        title="Days indoors by employment status",
        barmode='group' if len(countries) > 1 else 'relative',
        margin={"r": 0, "t": 50, "l": 0, "b": 0},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(
            title="Percentage of respondents",
            tickmode='array',
            tickvals=list(range(-100, 101, 10)),
            ticktext=list(range(100, -1, -10)) + list(range(10, 101, 10))
        ),
        annotations=[
            dict(x=-5, y=-1, text="Employed", showarrow=False, xanchor="right"),
            dict(x=5, y=-1, text="Self-employed", showarrow=False, xanchor="left")
        ],
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        font_family="Roboto", font_color="black"
    )

    return fig
