import pandas as pd

from .data_loader import get_data


def analyze_data_quality(df=None):
    """
    Comprehensive data quality analysis for all columns.
    
    Args:
        df (pd.DataFrame, optional): DataFrame to analyze. If None, loads from data_loader.
    
    Returns:
        dict: Quality report with findings for each column
    """
    if df is None:
        df = get_data()
    
    report = {
        'dataset_shape': df.shape,
        'columns': {}
    }
    
    # Analyze each column
    for col in df.columns:
        col_data = df[col]
        
        # Basic stats
        col_info = {
            'dtype': str(col_data.dtype),
            'total_rows': len(col_data),
            'non_null_count': col_data.notna().sum(),
            'null_count': col_data.isnull().sum(),
            'null_pct': round((col_data.isnull().sum() / len(col_data) * 100), 2),
            'unique_count': col_data.nunique(),
            'empty_string_count': (col_data == '').sum() if col_data.dtype == 'object' else 0,
        }
        
        # Sample values
        if col_data.dtype == 'object':
            sample_dist = col_data.value_counts(dropna=False).head(10).to_dict()
            col_info['top_values'] = sample_dist
            col_info['has_na_values'] = any(pd.isna(k) for k in sample_dist.keys())
        else:
            col_info['min'] = col_data.min()
            col_info['max'] = col_data.max()
            col_info['mean'] = col_data.mean()
        
        report['columns'][col] = col_info
    
    return report


def print_quality_report(report):
    """Pretty-print the comprehensive quality report for all columns."""
    shape = report['dataset_shape']
    print("\n" + "="*80)
    print("DATA QUALITY ANALYSIS REPORT - ALL COLUMNS")
    print("="*80)
    print(f"\nDataset Shape: {shape[0]} rows x {shape[1]} columns")
    print("\n" + "-"*80)
    
    for col, info in report['columns'].items():
        print(f"\n[{col}]")
        print(f"  Data Type: {info['dtype']}")
        print(f"  Non-null: {info['non_null_count']} | Null: {info['null_count']} ({info['null_pct']}%)")
        print(f"  Unique Values: {info['unique_count']}")
        
        if info['empty_string_count'] > 0:
            print(f"  Empty Strings: {info['empty_string_count']}")
        
        if 'top_values' in info:
            print(f"  Sample Values:")
            for val, count in list(info['top_values'].items())[:5]:
                val_display = str(val) if not pd.isna(val) else "[NULL/NaN]"
                print(f"    - {val_display}: {count}")
            if len(info['top_values']) > 5:
                print(f"    ... and {len(info['top_values']) - 5} more unique values")
        else:
            print(f"  Statistics: min={info['min']}, max={info['max']}, mean={info['mean']:.2f}")
    
    print("\n" + "="*80)


def print_categorical_columns(df=None):
    """
    Print all categories for each categorical column in the dataframe.
    
    Args:
        df (pd.DataFrame, optional): DataFrame to analyze. If None, loads from data_loader.
    """
    if df is None:
        df = get_data()
    
    print("\n" + "="*80)
    print("CATEGORICAL COLUMNS - ALL CATEGORIES")
    print("="*80)
    
    categorical_cols = df.select_dtypes(include=['category']).columns
    
    if len(categorical_cols) == 0:
        print("\nNo categorical columns found.")
        print("="*80 + "\n")
        return
    
    for col in categorical_cols:
        categories = df[col].cat.categories.tolist()
        print(f"\n[{col}] ({len(categories)} categories)")
        print(f"  {', '.join(str(c) for c in categories)}")
    
    print("\n" + "="*80 + "\n")


def clean_and_convert_types(df=None):
    """
    Clean data and apply all type conversions.
    
    Cleaning steps:
    - self_employed: Fill missing values with 'Unknown' category
    - Timestamp: Parse to datetime
    - All text columns: Convert to categorical (memory efficiency)
    
    Args:
        df (pd.DataFrame, optional): DataFrame to clean. If None, loads from data_loader.
    
    Returns:
        pd.DataFrame: Cleaned dataframe with proper types
    """
    if df is None:
        df = get_data().copy()
    else:
        df = df.copy()
    
    # 1. HANDLE MISSING self_employed (5,202 rows, 1.78%)
    missing_count = df['self_employed'].isnull().sum()
    df['self_employed'] = df['self_employed'].fillna('Unknown')
    
    # 2. DATETIME CONVERSION
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%m/%d/%Y %H:%M')
    
    # 3. CATEGORICAL CONVERSIONS (reduce memory usage)
    categorical_cols = [
        'Gender', 'Country', 'Occupation', 'self_employed',
        'family_history', 'treatment', 'Days_Indoors', 
        'Growing_Stress', 'Changes_Habits', 'Mental_Health_History',
        'Mood_Swings', 'Coping_Struggles', 'Work_Interest', 'Social_Weakness',
        'mental_health_interview', 'care_options'
    ]
    
    for col in categorical_cols:
        if col in df.columns:
            df[col] = df[col].astype('category')
        
    # Print summary
    memory_mb = df.memory_usage(deep=True).sum() / 1024**2

    
    return df


# ============================================================================
# SECTION 4: CHOROPLETH DATA AGGREGATION
# ============================================================================

def get_available_metrics():
    """
    Return metric definitions for choropleth visualization.
    
    Each metric is derived from Yes/No/Maybe categorical columns,
    converted to percentage values (0-100).
    
    Returns:
        dict: Metric names mapped to (column, target_value) tuples
              Example: {'treatment_rate': ('treatment', 'Yes'), ...}
    """
    return {
        'self_employment_rate': ('self_employed', 'Yes'),
        'treatment_rate': ('treatment', 'Yes'),
        'family_history_rate': ('family_history', 'Yes'),
        'growing_stress_rate': ('Growing_Stress', 'Yes'),
        'changes_habits_rate': ('Changes_Habits', 'Yes'),
        'mental_health_history_rate': ('Mental_Health_History', 'Yes'),
        'high_mood_swings_rate': ('Mood_Swings', 'High'),
        'work_interest_rate': ('Work_Interest', 'Yes'),
        'coping_struggles_rate': ('Coping_Struggles', 'Yes'),
        'social_weakness_rate': ('Social_Weakness', 'Yes'),
        'care_options_available_rate': ('care_options', 'Yes'),
        'mental_health_interview_rate': ('mental_health_interview', 'Yes')
    }


def get_choropleth_data(df, metric):
    """
    Prepare one metric per country for choropleth visualization.
    
    Calculates percentage of "Yes" responses grouped by country.
    
    Args:
        df (pd.DataFrame): Cleaned dataframe from clean_and_convert_types()
        metric (str): One of get_available_metrics().keys()
    
    Returns:
        pd.DataFrame: Three columns [Country, metric_value, respondents]
                     - Country: str (country name)
                     - metric_value: float (0-100, percentage)
                     - respondents: int (number of respondents per country)
    
    Raises:
        ValueError: If metric not in available metrics
    
    Example:
        >>> df_choropleth = get_choropleth_data(df_clean, 'treatment_rate')
        >>> df_choropleth
              Country  metric_value  respondents
        0  United States          50.2        1000
        1  United Kingdom          48.5         800
        2       Canada             52.1         600
    """
    metric_mappings = get_available_metrics()
    if metric not in metric_mappings:
        raise ValueError(f"Metric '{metric}' not in available metrics: {list(metric_mappings.keys())}")
    
    column, target_value = metric_mappings[metric]
    
    # Group by country and calculate percentage
    result_list = []
    for country in df['Country'].unique():
        country_df = df[df['Country'] == country]
        
        count_yes = (country_df[column] == target_value).sum()
        total = len(country_df)
        percentage = (count_yes / total * 100) if total > 0 else 0
        
        result_list.append({
            'Country': country,
            'metric_value': round(percentage, 2),
            'respondents': total
        })
    
    result_df = pd.DataFrame(result_list).sort_values('Country').reset_index(drop=True)
    return result_df


def get_country_metric_value(df, country, metric):
    """
    Get metric value and respondent count for one country (for popup display).
    
    Args:
        df (pd.DataFrame): Cleaned dataframe from clean_and_convert_types()
        country (str): Country name (must exist in Country column)
        metric (str): One of get_available_metrics().keys()
    
    Returns:
        dict: {'metric_value': float (0-100), 'respondents': int}
              Returns {'metric_value': 0.0, 'respondents': 0} if country not found
    
    Example:
        >>> result = get_country_metric_value(df_clean, 'United States', 'treatment_rate')
        >>> print(f"Treatment rate in US: {result['metric_value']}% ({result['respondents']} respondents)")
        Treatment rate in US: 50.2% (1234 respondents)
    """
    metric_mappings = get_available_metrics()
    if metric not in metric_mappings:
        raise ValueError(f"Metric '{metric}' not in available metrics: {list(metric_mappings.keys())}")
    
    column, target_value = metric_mappings[metric]
    
    # Filter to country data
    if country:
        country_df = df[df['Country'] == country]
    else:
        country_df = df
    
    if country_df.empty:
        return {'metric_value': 0.0, 'respondents': 0}
    
    # Calculate metric for this country only
    count_yes = (country_df[column] == target_value).sum()
    total = len(country_df)
    percentage = (count_yes / total * 100) if total > 0 else 0
    
    return {
        'metric_value': round(percentage, 2),
        'respondents': total
    }


# ============================================================================
# SECTION 5: RADAR CHART DATA AGGREGATION
# ============================================================================

def get_radar_data(df, country1=None, country2=None):
    """
    Prepare data for radar chart visualization (4 mental health metrics).
    
    Metrics included: growing stress, mood swings, coping struggles, social weakness.
    
    Args:
        df (pd.DataFrame): Cleaned dataframe from clean_and_convert_types()
        country1 (str): First country name
        country2 (str, optional): Second country name for comparison overlay
    
    Returns:
        dict: Structure for Plotly radar chart with keys:
              - 'metrics': list of metric names
              - 'country1': dict with 'name' and 'values' (list of percentages)
              - 'country2': dict with 'name' and 'values' (or None if not provided)
    
    Example:
        >>> radar_data = get_radar_data(df_clean, 'United States', 'Canada')
        >>> radar_data
        {
            'metrics': ['Growing Stress', 'High Mood Swings', 'Coping Struggles', 'Social Weakness'],
            'country1': {'name': 'United States', 'values': [33.5, 31.2, 47.5, 31.3]},
            'country2': {'name': 'Canada', 'values': [33.8, 31.1, 47.2, 31.4]}
        }
    """
    radar_metrics = [
        'growing_stress_rate',
        'high_mood_swings_rate',
        'coping_struggles_rate',
        'social_weakness_rate'
    ]
    
    metric_labels = [
        'Growing Stress',
        'High Mood Swings',
        'Coping Struggles',
        'Social Weakness'
    ]
    
    # Get values for country1
    country1_values = []
    for metric in radar_metrics:
        result = get_country_metric_value(df, country1, metric)
        country1_values.append(result['metric_value'])
    
    if country1 is None:
        country1 = "Global"
        
    radar_data = {
        'metrics': metric_labels,
        'country1': {
            'name': country1,
            'values': country1_values
        },
        'country2': None
    }
    
    # Get values for country2 if provided
    if country2:
        country2_values = []
        for metric in radar_metrics:
            result = get_country_metric_value(df, country2, metric)
            country2_values.append(result['metric_value'])
        
        radar_data['country2'] = {
            'name': country2,
            'values': country2_values
        }
    
    return radar_data


# ============================================================================
# SECTION 6: BUTTERFLY CHART DATA AGGREGATION
# ============================================================================

def get_butterfly_data(df, country1=None, country2=None):
    """
    Prepare data for butterfly chart (employment status vs days indoors).
    
    Butterfly chart shows employment status (self-employed vs employed) on two sides,
    with Days_Indoors categories on the vertical axis. Horizontal bars show percentages
    within each employment status category.
    
    Args:
        df (pd.DataFrame): Cleaned dataframe from clean_and_convert_types()
        country1 (str): First country name
        country2 (str, optional): Second country name for stacked comparison
    
    Returns:
        dict: Structure for Plotly butterfly chart with keys:
              - 'days_indoors_order': list of Days_Indoors categories in logical order
              - 'country1': dict with 'name' and nested dicts for 'employed' and 'self_employed'
                           Each contains percentages per Days_Indoors category
              - 'country2': dict with same structure (or None if not provided)
    
    Example:
        >>> butterfly_data = get_butterfly_data(df_clean, 'United States')
        >>> butterfly_data
        {
            'days_indoors_order': ['Go out Every day', '1-14 days', '15-30 days', '31-60 days', 'More than 2 months'],
            'country1': {
                'name': 'United States',
                'employed': {'Go out Every day': 33.5, '1-14 days': 28.2, ...},
                'self_employed': {'Go out Every day': 35.1, '1-14 days': 26.8, ...}
            },
            'country2': None
        }
    """
    # Logical order for Days_Indoors (least to most time indoors)
    days_indoors_order = [
        'Go out Every day',
        '1-14 days',
        '15-30 days',
        '31-60 days',
        'More than 2 months'
    ]
    
    def aggregate_butterfly_for_country(country_df):
        """Helper function to aggregate butterfly data for one country."""
        employment_types = {
            'employed': 'No',        # self_employed == 'No'
            'self_employed': 'Yes'   # self_employed == 'Yes'
        }
        
        result = {}
        
        for emp_type, emp_value in employment_types.items():
            emp_df = country_df[country_df['self_employed'] == emp_value]
            total_emp = len(emp_df)
            
            # Calculate percentages for each Days_Indoors category
            percentages = {}
            for day_cat in days_indoors_order:
                count = (emp_df['Days_Indoors'] == day_cat).sum()
                pct = (count / total_emp * 100) if total_emp > 0 else 0.0
                percentages[day_cat] = round(pct, 2)
            
            result[emp_type] = percentages
        

        return result
    
    # Get data for country1
    if country1:
        country1_df = df[df['Country'] == country1]
        country1_name = country1
    else:
        country1_df = df
        country1_name = "Global"

    country1_agg = aggregate_butterfly_for_country(country1_df)
    
    butterfly_data = {
        'days_indoors_order': days_indoors_order,
        'country1': {
            'name': country1_name,
            'employed': country1_agg['employed'],
            'self_employed': country1_agg['self_employed']
        },
        'country2': None
    }
    
    # Get data for country2 if provided
    if country2:
        country2_df = df[df['Country'] == country2]
        country2_agg = aggregate_butterfly_for_country(country2_df)
        
        butterfly_data['country2'] = {
            'name': country2,
            'employed': country2_agg['employed'],
            'self_employed': country2_agg['self_employed']
        }
    
    return butterfly_data


# ============================================================================
# SECTION 7: STACKED BAR CHART DATA AGGREGATION
# ============================================================================

def get_stacked_bar_data(df, country1=None, country2=None):
    """
    Prepare data for horizontal stacked bar chart (mental health interview vs social weakness).
    
    Each bar represents a mental_health_interview response and shows the distribution of 
    Social_Weakness categories as percentages.
    
    Args:
        df (pd.DataFrame): Cleaned dataframe from clean_and_convert_types()
        country1 (str): First country name
        country2 (str, optional): Second country name for stacked display below
    
    Returns:
        dict: Structure for Plotly horizontal stacked bar chart with keys:
              - 'social_weakness_order': list of Social_Weakness categories in logical order
              - 'interview_responses': list of mental_health_interview response types
              - 'country1': dict with 'name' and nested dicts for each mental_health_interview response
                           Each contains percentages per social weakness category
              - 'country2': dict with same structure (or None if not provided)
    
    Example:
        >>> stacked_data = get_stacked_bar_data(df_clean, 'United States')
        >>> stacked_data
        {
            'social_weakness_order': ['No', 'Maybe', 'Yes'],
            'interview_responses': ['No', 'Maybe', 'Yes'],
            'country1': {
                'name': 'United States',
                'No': {'No': 48.1, 'Maybe': 18.5, 'Yes': 19.2},
                'Maybe': {'No': 45.2, 'Maybe': 20.1, 'Yes': 19.4},
                'Yes': {'No': 42.3, 'Maybe': 22.1, 'Yes': 18.8}
            },
            'country2': None
        }
    """
    # Logical order for Social_Weakness
    social_weakness_order = ['No', 'Maybe', 'Yes']
    
    # Logical order for mental health interview responses
    interview_responses_order = ['No', 'Maybe', 'Yes']
    
    def aggregate_stacked_bar_for_country(country_df):
        """Helper function to aggregate stacked bar data for one country."""
        result = {}
        
        for weakness_cat in social_weakness_order:
            weakness_df = country_df[country_df['Social_Weakness'] == weakness_cat]
            total = len(weakness_df)

            percentages = {}
            for response in interview_responses_order:
                count = (weakness_df['mental_health_interview'] == response).sum()
                pct = (count / total * 100) if total > 0 else 0.0
                percentages[response] = round(pct, 2)

            result[weakness_cat] = percentages

        return result
    
    # Get data for country1
    if country1:
        country1_df = df[df['Country'] == country1]

    else:
        country1 = "Global"
        country1_df = df

    country1_agg = aggregate_stacked_bar_for_country(country1_df)
    
    stacked_data = {
        'interview_responses': interview_responses_order,
        'social_weakness_order': social_weakness_order,
        'country1': {
            'name': country1,
            **country1_agg
        },
        'country2': None
    }
    
    # Get data for country2 if provided
    if country2:
        country2_df = df[df['Country'] == country2]
        country2_agg = aggregate_stacked_bar_for_country(country2_df)
        
        stacked_data['country2'] = {
            'name': country2,
            **country2_agg
        }
    
    return stacked_data
