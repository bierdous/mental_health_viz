import plotly.express as px


"""
Custom titles for choropleth maps based on the selected metric.
"""

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

def create_choropleth(df, metric_label):
    """
    Create a choropleth map visualization.
    
    Args:
        df (pd.DataFrame): Dataframe returned by get_choropleth_data
                          Columns: [Country, metric_value, respondents]
        metric_label (str): Label for the metric to display in title/legend
    
    Returns:
        plotly.graph_objects.Figure: Choropleth map figure
    """
    fig = px.choropleth(
        df,
        locations="Country",
        locationmode="country names",
        color="metric_value",
        hover_name="Country",
        hover_data={
            "Country": False,
            "metric_value": ":.2f",
            "respondents": True
        },
        color_continuous_scale="YlGnBu",
        labels={
            "metric_value": "Share of Respondents (%)",
            "respondents": "Number of Respondents"
        },
        title=CHOROPLETH_TITLES[metric_label]
    )
    
    fig.update_layout(
        margin={"r": 0, "t": 50, "l": 0, "b": 0},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='equirectangular',
            bgcolor="rgba(0,0,0,0)"
        ),  
        font_family="Roboto",
        font_color="black"
    )
    
    fig.update_traces(hoverinfo='none', hovertemplate=None)
    return fig