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
        className="grid",
        children=[

            # Header (title)
            html.Div(
                className="header",
                children=html.H1("Mental Health")
            ),

            # Controls
            html.Div(
                className="controls",
                children=[
                    html.H3("Selected countries"),

                    html.Div(
                        className="country-row",
                        children=[
                            html.Span("None", id="country-a", className="country-label"),
                            html.Button("Clear", id="clear-a", className="clear-btn"),
                        ]
                    ),

                    html.Div(
                        className="country-row",
                        children=[
                            html.Span("None", id="country-b", className="country-label"),
                            html.Button("Clear", id="clear-b", className="clear-btn")
                        ]
                    ),
                ]
            ),

<<<<<<< HEAD
            # Top middle graph
            html.Div(
                className="graph-top",
                children=dcc.Graph(id="graph-top")
=======
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
>>>>>>> ed5d868946611ab4e11d156100cac7fa26c8fffe
            ),

            # Butterfly
            html.Div(
                className="butterfly",
                children=dcc.Graph(id="butterfly")
            ),

            # Choropleth
            html.Div(
                className="map",
                children=dcc.Graph(id="choropleth")
            ),

            # Text
            html.Div(
                className="text",
                children=html.Div("To pass the course you need to complete the semestral project and pass the written exam. You have to obtain at least 26 points (out of 50 possible) on the final written exam. In addition, if you have any positive points from the project work, these can improve your final grade. On the other hand, if you have any negative points, these will be subtracted from your exam score. The grading scale based on your final score is the following:")
            ),

            # Radar
            html.Div(
                className="radar",
                children=dcc.Graph(id="radar")
            ),
        ]
    )
