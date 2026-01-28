import plotly.graph_objects as go
from plotly.subplots import make_subplots
from ..theme import STACKED_CHART_COLOR, CHART_TITLE_STYLE

def create_stacked_bar_chart(stacked_data):
    """
    Create horizontal stacked bar chart showing:
    Social Weakness (Y) vs Mental Health Interview (stacked).
    
    Supports one or two countries (displayed vertically).
    """

    countries = [stacked_data["country1"]]
    if stacked_data["country2"]:
        countries.append(stacked_data["country2"])
    

    social_weakness_order = stacked_data["social_weakness_order"]
    interview_responses_order = stacked_data["interview_responses"]


    fig = make_subplots(
        rows=len(countries),
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.15,
        subplot_titles=[c["name"] for c in countries]
    )

    for row, country in enumerate(countries, start=1):
        for interview in interview_responses_order:
            # Pro každý Social_Weakness získáme procenta dané odpovědi
            values = [country[weakness][interview] for weakness in social_weakness_order]

            text_values = [interview if v > 0 else "" for v in values]

            fig.add_trace(
                go.Bar(
                    y=social_weakness_order,     # Y = Social_Weakness
                    x=values,                    # X = %
                    orientation="h",
                    name=interview,              # stack = mental_health_interview
                    marker_color=STACKED_CHART_COLOR['country1'][interview] if country['name'] == countries[0]['name'] else STACKED_CHART_COLOR['country2'][interview],
                    text=text_values,               # zobrazit text uvnitř segmentu
                    textposition='inside',          # pozice uvnitř
                    insidetextanchor='middle',      # zarovnání textu uprostřed segmentu
                    showlegend=False,               # legendu už nepotřebujeme
                    hovertemplate=(
                        "Social weakness: %{y}<br>"
                        "Interview: " + interview + "<br>"
                        "Percentage: %{x}%<extra></extra>"
                    )
                ),
                row=row,
                col=1
            )

    fig.update_layout(
        barmode="stack",
        title=dict(
            text="Mental Health Disclosure in Relation to Social Weakness",
            **CHART_TITLE_STYLE
            ),
        height=300 * len(countries),
        margin=dict(l=90, r=30, t=65, b=30),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend_title="Mental Health Interview",
        font_family="Roboto", font_color="black"
    )

    fig.update_xaxes(
        title_text="Share of Respondents (%)",
        row=len(countries),
        col=1,
        range=[0, 100]
    )

    fig.add_annotation(
        x=-0.18,                       # posun doleva od grafu (mimo plot)
        y=0.5,                          # uprostřed figure
        xref='paper',
        yref='paper',
        text='Social Weakness',
        showarrow=False,
        textangle=-90,                  # otočit text vertikálně
        font=dict(size=14)
    )

    return fig