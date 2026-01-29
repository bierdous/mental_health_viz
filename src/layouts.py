from dash import html, dcc
import dash_bootstrap_components as dbc

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


# Metric options for popup description (value -> label)
POPUP_DESC = [
    {'value': 'treatment_rate', 'label': 'seeked treatment'},
    {'value': 'self_employment_rate', 'label': 'are self-employed'},
    {'value': 'family_history_rate', 'label': 'have a family history of mental illness'},
    {'value': 'growing_stress_rate', 'label': 'experience growing stress'},
    {'value': 'changes_habits_rate', 'label': 'changed their habits'},
    {'value': 'mental_health_history_rate', 'label': 'have a personal history of mental illness'},
    {'value': 'high_mood_swings_rate', 'label': 'experience high mood swings'},
    {'value': 'work_interest_rate', 'label': 'have an interest in their work'},
    {'value': 'coping_struggles_rate', 'label': 'struggle to cope'},
    {'value': 'social_weakness_rate', 'label': 'experience social weakness'},
    {'value': 'care_options_available_rate', 'label': 'are aware of employer offered care options'},
    {'value': 'mental_health_interview_rate', 'label': 'would open up about mental health at an interview'},
]


CHOROPLETH_TITLES = {
    'treatment_rate': "Seeking Treatment for Mental Health Issues",
    'self_employment_rate': "Self-Employment",
    'family_history_rate': "Family History of Mental Health Issues",
    'growing_stress_rate': "Perceived Growing Stress Levels",
    'changes_habits_rate': "Perceived Changes in Habits",
    'mental_health_history_rate': "Personal History of Mental Health Issues",
    'high_mood_swings_rate': "Perceived High Mood Swings",
    'work_interest_rate': "Reported Work Interest",
    'coping_struggles_rate': "Reported Struggle to Cope",
    'social_weakness_rate': "Reported Social Weakness",
    'care_options_available_rate': "Awareness of Care Options Provided by Employer",
    'mental_health_interview_rate': "Willigness to Bring Up Mental Health in an Interview"
}

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
                                            html.Div("Mental Health Dashboard", className="mental-health"),
                                            html.Div(className="info-btns", children=[
                                               dbc.Button(
                                                    children=[
                                                        html.I(className="bi bi-info-lg"),
                                                    ],
                                                    id="about-btn",
                                                    color="light",
                                                    n_clicks=0,
                                                ),
                                                dbc.Popover(
                                                    [
                                                        dbc.PopoverHeader("About the dashboard"),
                                                        dbc.PopoverBody([
                                                            html.H5("Dataset"),
                                                            html.P([
                                                                "This dashboard utilizes a dataset regarding mental health in the tech workplace. ",
                                                                "You can find the dataset ",
                                                                html.A("here", href="https://www.kaggle.com/datasets/bhavikjikadara/mental-health-dataset", target="_blank"),
                                                                "."
                                                            ]),
                                                            html.P("The dataset contains survey responses from employees in the tech sector, covering various aspects of mental health and workplace culture."),
                                                            
                                                            html.H5("Reliability Disclaimer"),
                                                            html.P("Please note that this dataset is not reliable. It was copied from another source, and rows were artificially added to increase the data volume."),
                                                            
                                                            html.H5("Data Transformations"),
                                                            html.Ul([
                                                                html.Li("Missing values in the 'self_employed' column were replaced with an 'Unknown' category to maintain data integrity."),
                                                            ]),

                                                            html.H5("Views"),
                                                            html.P("The dashboard presents data through several views: a world map for global overview, and comparative charts (stacked bar, butterfly, radar) for detailed analysis of selected countries."),

                                                            html.H5("Authors"),
                                                            html.P("Marek Dohnal, Petr Polách"),
                                                            html.P("Created for the Visualization course at Faculty of Informatics, MUNI, 2026"),
                                                        ]),
                                                    ],
                                                    target="about-btn",
                                                    trigger="click",
                                                    style={"maxWidth": "600px"},
                                                ), 
                                                dbc.Button(
                                                    children=[
                                                        html.I(className="bi bi-question-lg"),
                                                    ],
                                                    color="light",
                                                    id="use-btn",
                                                    n_clicks=0,
                                                ),
                                                dbc.Popover(
                                                    [
                                                        dbc.PopoverHeader("How to use the dashboard"),
                                                        dbc.PopoverBody([
                                                            html.H5("Interactivity"),
                                                            html.Ul([
                                                                html.Li("Select a country by clicking on the map, then choose 'Select as first' or 'Select as second'."),
                                                                html.Li("Compare up to two countries to see detailed charts update automatically."),
                                                                html.Li("Change the mapped metric using the 'Mental health indicator' dropdown."),
                                                                html.Li("Remove a country selection by clicking the trash icon."),
                                                            ]),
                                                            
                                                            html.H5("Views"),
                                                            html.B("World Map"),
                                                            html.P("Displays the global distribution of the selected mental health indicator."),
                                                            
                                                            html.B("Stacked Bar Chart"),
                                                            html.P("Shows how social weakness influences the likelihood to mention mental health issues at an interview."),
                                                            
                                                            html.B("Butterfly Chart"),
                                                            html.P("Contrasts the 'Time Spent Indoors' for employed vs. self-employed respondents."),
                                                            
                                                            html.B("Radar Chart"),
                                                            html.P("Provides a holistic comparison of multiple key mental health metrics simultaneously."),
                                                        ]),
                                                    ],
                                                    target="use-btn",
                                                    trigger="click",
                                                    style={"maxWidth": "600px"},
                                                ),
                                            ])
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
                                                                            html.I(className="bi bi-trash-fill")
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
                                                                            html.I(className="bi bi-trash-fill")
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
                                                    dcc.Store(id='sel-metric-store', data='treatment_rate'),
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
                                            )
                                            # Map Detail Toggle
                                            # html.Div(
                                            #     className="map-detail",
                                            #     children=[
                                            #         html.Div("Map detail", className="toggles-label"),
                                            #         html.Div(
                                            #             className="detail-picker",
                                            #             children=[
                                            #                 html.Div(
                                            #                     className="trailing-accessories",
                                            #                     children=[
                                            #                         html.Div("Continent", className="label"),
                                            #                         html.Div(
                                            #                             className="push-button",
                                            #                             children=[
                                            #                                 html.Div(
                                            #                                     className="bg",
                                            #                                     children=[html.Div(className="black")]
                                            #                                 ),
                                            #                                 html.Div("Country", className="label2")
                                            #                             ]
                                            #                         )
                                            #                     ]
                                            #                 )
                                            #             ]
                                            #         )
                                            #     ]
                                            # )
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
                            html.Div(
                                id="choropleth-title",
                                children=CHOROPLETH_TITLES['treatment_rate'],
                                className="choropleth-title"
                            ),
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
                                className="popup",
                                style={"display": "none"},
                                children=[
                                    html.Div(className="header", children=[
                                        html.Div("Angola", id="header-text", className="header-text"),
                                        html.Div(className="close", id="popup-close",
                                            children=[
                                                html.I(className="bi bi-x-lg")
                                            ])
                                    ]),
                                    html.Div(className="percentage-metric", children=[
                                        html.Div("23%", id="percentage", className="percentage"),
                                        html.Div("Seeking Treatment", id="metric-desc", className="metric-desc")
                                    ]),
                                    html.Div(className="sel-btn-area",
                                        children=[
                                            dbc.Button("Select as first", id="btn-sel1", n_clicks=0, className="sel-btn sel-btn1-bg"),
                                            dbc.Button("Select as second", id="btn-sel2", n_clicks=0, className="sel-btn sel-btn2-bg")
                                        ])
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
