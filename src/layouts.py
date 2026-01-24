from dash import html, dcc

def create_layout():
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

            # Top middle graph
            html.Div(
                className="graph-top",
                children=dcc.Graph(id="graph-top")
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
