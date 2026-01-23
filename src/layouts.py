from dash import html, dcc

# Metric options for dropdown (value -> label)
METRIC_OPTIONS = [
    {'value': 'treatment_rate', 'label': 'Treatment Rate'},
    {'value': 'self_employment_rate', 'label': 'Self-Employment Rate'},
    {'value': 'family_history_rate', 'label': 'Family History Rate'},
    {'value': 'growing_stress_rate', 'label': 'Growing Stress Rate'},
    {'value': 'changes_habits_rate', 'label': 'Changes in Habits Rate'},
    {'value': 'mental_health_history_rate', 'label': 'Mental Health History Rate'},
    {'value': 'high_mood_swings_rate', 'label': 'High Mood Swings Rate'},
    {'value': 'work_interest_rate', 'label': 'Work Interest Rate'},
    {'value': 'coping_struggles_rate', 'label': 'Coping Struggles Rate'},
    {'value': 'social_weakness_rate', 'label': 'Social Weakness Rate'},
    {'value': 'care_options_available_rate', 'label': 'Care Options Available Rate'},
    {'value': 'mental_health_interview_rate', 'label': 'Mental Health Interview Rate'},
]


def create_layout(figures=None):
    if figures is None:
        figures = {}
    
    return html.Div(
        className="container",
        children=[

            # Header
            html.Div(
                className="header",
                children=[
                    html.H1("Mental Health"),
                ]
            ),

            # Map row
            html.Div(
                className="row",
                children=[
                    html.Div(
                        className="graph large",
                        children=[
                            # Dropdown for metric selection
                            html.Div(
                                className="dropdown-container",
                                children=[
                                    dcc.Dropdown(
                                        id="metric-dropdown",
                                        options=METRIC_OPTIONS,
                                        value='treatment_rate',
                                        clearable=False,
                                        className="metric-dropdown"
                                    )
                                ]
                            ),
                            # Choropleth map
                            dcc.Graph(
                                id="choropleth",
                                figure=figures.get('choropleth', {})
                            )
                        ]
                    ),
                    html.Div(
                        className="graph medium",
                        children=dcc.Graph(id="butterfly")
                    )
                ]
            ),

            # Row 2
            html.Div(
                className="row",
                children=[
                    html.Div(
                        className="graph medium",
                        children=dcc.Graph(id="radar")
                    ),
                    html.Div(
                        className="graph medium",
                        children=dcc.Graph(id="additional")
                    )
                ]
            )
        ]
    )