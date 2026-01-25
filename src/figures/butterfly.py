import plotly.graph_objects as go

def create_butterfly_chart(butterfly_data, country2=False):

    def create_1_country_butterfly_chart():
        days = butterfly_data['days_indoors_order']

        employed = [
            butterfly_data['country1']['employed'][d]
            for d in days
        ]

        self_employed = [
            butterfly_data['country1']['self_employed'][d]
            for d in days
        ]

        employed_neg = [-v for v in employed]

        fig = go.Figure()

        fig.add_trace(go.Bar(
            y=days,
            x=employed_neg,
            name='Employed',
            orientation='h',
            customdata=employed,
            hovertemplate='%{y}: %{customdata}',
            showlegend=False
        ))

        fig.add_trace(go.Bar(
            y=days,
            x=self_employed,
            name='Self-employed',
            orientation='h',
            hovertemplate='%{y}: %{x}',
            showlegend=False
        ))
    
        fig.update_layout(
            title=f"Days indoors by employment status",
            barmode='relative',
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
            )
        )
        return fig
    
    def create_2_country_butterfly_chart():
        days = butterfly_data['days_indoors_order']

        c1_emp = [-butterfly_data['country1']['employed'][d] for d in days]
        c1_self = [butterfly_data['country1']['self_employed'][d] for d in days]

        # Country 2
        c2_emp = [-butterfly_data['country2']['employed'][d] for d in days]
        c2_self = [butterfly_data['country2']['self_employed'][d] for d in days]



        fig = go.Figure()

        # LEFT SIDE – Employed
        fig.add_trace(go.Bar(
            y=days,
            x=c1_emp,
            name=butterfly_data['country1']['name'],
            orientation="h",
            marker_color="#1f77b4",
            customdata=[abs(v) for v in c1_emp],
            hovertemplate="%{y}<br>%{customdata}%<extra></extra>",
            showlegend=True
            ))

        fig.add_trace(go.Bar(
            y=days,
            x=c2_emp,
            name=butterfly_data['country2']['name'],
            orientation="h",
            marker_color="#d62728",
            customdata=[abs(v) for v in c2_emp],
            hovertemplate="%{y}<br>%{customdata}%<extra></extra>",
            showlegend=True
        ))

        # RIGHT SIDE – Self-employed
        fig.add_trace(go.Bar(
            y=days,
            x=c1_self,
            orientation="h",
            marker_color="#1f77b4",
            hovertemplate="%{y}<br>%{x}%<extra></extra>",
            showlegend=False
        ))

        fig.add_trace(go.Bar(
            y=days,
            x=c2_self,
            orientation="h",
            marker_color="#d62728",
            hovertemplate="%{y}<br>%{x}%<extra></extra>",
            showlegend=False
        ))

        fig.update_layout(
            barmode="group",   # tady musí být "group", aby se sloupce zemí vedle sebe
            xaxis=dict(
                title="Percentage of respondents",
                tickvals=list(range(-100, 101, 10)),
                ticktext=list(range(100, -1, -10)) + list(range(10, 101, 10))
            ),
            yaxis=dict(
                autorange="reversed"  # aby nejnižší kategorie byla dole
            ),
            annotations=[
                dict(x=-5, y=-1, text="Employed", showarrow=False, xanchor="right"),
                dict(x=5, y=-1, text="Self-employed", showarrow=False, xanchor="left")
            ],
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            margin=dict(l=0, r=0, t=40, b=0)
        )
        return fig


    if country2:
        return create_2_country_butterfly_chart()

    else:
        return create_1_country_butterfly_chart()

