import plotly.graph_objects as go
from plotly.subplots import make_subplots

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

    # Barvy pro mental_health_interview
    colors = {
        "No": "#1f77b4",
        "Maybe": "#ff7f0e",
        "Yes": "#2ca02c"
    }

    fig = make_subplots(
        rows=len(countries),
        cols=1,
        shared_xaxes=True,
        subplot_titles=[c["name"] for c in countries]
    )

    for row, country in enumerate(countries, start=1):
        for interview in interview_responses_order:
            # Pro každý Social_Weakness získáme procenta dané odpovědi
            values = [country[weakness][interview] for weakness in social_weakness_order]

            fig.add_trace(
                go.Bar(
                    y=social_weakness_order,     # Y = Social_Weakness
                    x=values,                    # X = %
                    orientation="h",
                    name=interview,              # stack = mental_health_interview
                    marker_color=colors[interview],
                    showlegend=(row == 1),       # legenda jen u prvního grafu
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
        title="Mental Health Interview vs Social Weakness",
        xaxis_title="Percentage (%)",
        yaxis_title="Social Weakness",
        height=300 * len(countries),
        margin=dict(l=90, r=40, t=80, b=40),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend_title="Mental Health Interview"
    )

    fig.update_xaxes(range=[0, 100])  # škála X od 0 do 100%

    return fig