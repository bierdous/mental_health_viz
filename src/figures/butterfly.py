import plotly.graph_objects as go
from ..theme import COUNTRY_COLORS,CHART_TITLE_STYLE, FONT

def create_butterfly_chart(butterfly_data):

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
                marker_color=COUNTRY_COLORS['country1'] if country['name'] == countries[0]['name'] else COUNTRY_COLORS['country2'],
                hovertemplate='%{y}: %{customdata}',
                showlegend=True if status == 'employed' else False
            ))

    fig.update_layout(
        title=dict(
            text="Time Spent Indoors by Employment Status",
            **CHART_TITLE_STYLE
            ),
        barmode='group' if len(countries) > 1 else 'relative',
        margin=dict(r=30, t=65, l=30, b=30),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(
            title="Percentage of Respondents",
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
        font_family=FONT, font_color="black"
    )

    return fig
