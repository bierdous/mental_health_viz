from dash import html, dcc

# Metric options for dropdown (value -> label)
METRIC_OPTIONS = [
    {'value': 'treatment_rate', 'label': 'Seeking Treatment'},
    {'value': 'self_employment_rate', 'label': 'Self-Employment'},
    {'value': 'family_history_rate', 'label': 'Family History of Mental Illness'},
    {'value': 'growing_stress_rate', 'label': 'Growing Stress'},
    {'value': 'changes_habits_rate', 'label': 'Changes in Habits'},
    {'value': 'mental_health_history_rate', 'label': 'Mental Health History'},
    {'value': 'high_mood_swings_rate', 'label': 'Mood Swings'},
    {'value': 'work_interest_rate', 'label': 'Work Interest'},
    {'value': 'coping_struggles_rate', 'label': 'Coping Struggles'},
    {'value': 'social_weakness_rate', 'label': 'Social Weakness'},
    {'value': 'care_options_available_rate', 'label': 'Awareness of Employer Offered Care Options'},
    {'value': 'mental_health_interview_rate', 'label': 'Opening up About Mental Health at an Interview'},
]

def create_layout(figures=None):
    if figures is None:
        figures = {}
    
    return html.Div(
        id="dashboard",
        className="dashboard",
        children=[
            html.Div(id="output", style={"marginTop": "20px", "fontSize": "18px"}),
            # Left Panel
            html.Div(
                className="left-panel",
                children=[
                    # Toggles & Bar Chart Section
                    html.Div(
                        className="toggles-bar-chart",
                        children=[
                            # Toggles Area
                            html.Div(
                                className="toggles-area",
                                children=[
                                    # Title
                                    html.Div(
                                        className="title",
                                        children=[
                                            html.Div("Mental Health", className="mental-health")
                                        ]
                                    ),
                                    # Toggles Container
                                    html.Div(
                                        className="toggles",
                                        children=[
                                            # Selected Countries
                                            html.Div(
                                                className="selected-ctrs",
                                                children=[
                                                    html.Div("Selected countries", className="toggles-label"),
                                                    html.Div(
                                                        className="ctrs-label-area",
                                                        children=[
                                                            html.Div(
                                                                className="ctry-and-trash-icon",
                                                                id="ctry-1-container",
                                                                children=[
                                                                    html.Div(
                                                                        className="ctry ctry-1-bg",
                                                                        children=[
                                                                            html.Div("Empty", className="ctry-name", id="ctry-1-tag")
                                                                        ]
                                                                    ),
                                                                    html.Div(className="trash", id="ctry-1-trash",
                                                                        children=[
                                                                            html.Img(className="trash_svg", src="assets/trash.svg")
                                                                        ]
                                                                    )
                                                                ]
                                                            ),
                                                            html.Div(
                                                                className="ctry-and-trash-icon",
                                                                id="ctry-2-container",
                                                                children=[
                                                                    html.Div(
                                                                        className="ctry ctry-2-bg",
                                                                        children=[
                                                                            html.Div("Empty", className="ctry-name", id="ctry-2-tag")
                                                                        ]
                                                                    ),
                                                                    html.Div(className="trash", id="ctry-2-trash",
                                                                        children=[
                                                                            html.Img(className="trash_svg", src="assets/trash.svg")
                                                                        ]
                                                                    )
                                                                ]
                                                            )
                                                        ]
                                                    )
                                                ]
                                            ),
                                            # Metric Selector
                                            html.Div(
                                                className="metric-selector",
                                                children=[
                                                    html.Div("Mental health indicator", className="toggles-label"),
                                                    # Using Dash Dropdown instead of static HTML
                                                    html.Div(
                                                        className="dropdown-metric-area",
                                                        children=[
                                                            dcc.Dropdown(
                                                                id="metric-dropdown",
                                                                options=METRIC_OPTIONS,
                                                                value='treatment_rate',
                                                                clearable=False,
                                                                className="dropdown-metric",
                                                                maxHeight=300,
                                                                placeholder="Select..."
                                                            )
                                                        ]
                                                    )
                                                ]
                                            ),
                                            # Map Detail Toggle
                                            html.Div(
                                                className="map-detail",
                                                children=[
                                                    html.Div("Map detail", className="toggles-label"),
                                                    html.Div(
                                                        className="detail-picker",
                                                        children=[
                                                            html.Div(
                                                                className="trailing-accessories",
                                                                children=[
                                                                    html.Div("Continent", className="label"),
                                                                    html.Div(
                                                                        className="push-button",
                                                                        children=[
                                                                            html.Div(
                                                                                className="bg",
                                                                                children=[html.Div(className="black")]
                                                                            ),
                                                                            html.Div("Country", className="label2")
                                                                        ]
                                                                    )
                                                                ]
                                                            )
                                                        ]
                                                    )
                                                ]
                                            )
                                        ]
                                    )
                                ]
                            ),
                            # Stacked Bar Chart Area
                            html.Div(
                                className="stacked-bar-chart-area",
                                children=[
                                    html.Div(
                                        className="stacked-bar-chart",
                                        children=dcc.Graph(
                                            id="stacked-bar",
                                            figure=figures.get('stacked_bar', {}),
                                            responsive=True,
                                            style={'height': '100%', 'width': '100%'}
                                        )
                                    )
                                ]
                            )
                        ]
                    ),
                    # Choropleth Area
                    html.Div(
                        className="choropleth-area-bg",
                        children=[
                            # Stores the country immediately clicked (temporary)
                            dcc.Store(id='temp-click-store'),
                            # The final selections used by other charts
                            dcc.Store(id='selected-ctry1-store'),
                            dcc.Store(id='selected-ctry2-store'),
                            html.Div(
                                className="choropleth",
                                children=[dcc.Graph(
                                    id="choropleth", 
                                    figure=figures.get('choropleth', {}),
                                    responsive=True,
                                    style={'height': '100%', 'width': '100%'}
                            ),
                            html.Div(
                                id="popup",
                                style={"display": "none"},
                                children=[
                                    html.Div(id="popup-text", style={"marginBottom": "10px"}),

                                    html.Button("Set as Selected 1", id="btn-sel1", n_clicks=0,
                                                style={"marginRight": "10px"}),

                                    html.Button("Set as Selected 2", id="btn-sel2", n_clicks=0),
                                ]
                            ),
                            ]
                        )
                        ]
                    )
                ]
            ),
            # Right Panel
            html.Div(
                className="right-panel",
                children=[
                    # Butterfly Chart Area
                    html.Div(
                        className="butterfly-chart-area",
                        children=[
                            html.Div(
                                className="butterfly-chart",
                                children=dcc.Graph(
                                    id="butterfly",
                                    figure=figures.get('butterfly', {}),
                                    responsive=True,
                                    style={'height': '100%', 'width': '100%'}
                                )
                            )
                        ]
                    ),
                    # Radar Chart Area
                    html.Div(
                        className="radar",
                        children=dcc.Graph(
                            id="radar",
                            figure=figures.get('radar', {}),
                            responsive=True,
                            style={'height': '100%', 'width': '100%'}
                        )
                    )
                ]
            )
        ]    
    )
