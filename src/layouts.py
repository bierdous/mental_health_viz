from dash import html, dcc

def create_layout():
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

            # Map
            html.Div(
                className="row",
                children=[
                    html.Div(
                        className="graph large",
                        children=dcc.Graph(id="choropleth")
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