import pandas as pd
try:
    from .data_loader import get_data
except ImportError:
    from data_loader import get_data


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
    
    print("\n" + "="*70)
    print("DATA CLEANING AND TYPE CONVERSION")
    print("="*70)
    
    # 1. HANDLE MISSING self_employed (5,202 rows, 1.78%)
    missing_count = df['self_employed'].isnull().sum()
    df['self_employed'] = df['self_employed'].fillna('Unknown')
    print(f"\n[CLEAN] self_employed: Filled {missing_count} missing values with 'Unknown'")
    
    # 2. DATETIME CONVERSION
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%m/%d/%Y %H:%M')
    print("[CONVERT] Timestamp -> datetime64")
    
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
    
    print(f"[CONVERT] {len(categorical_cols)} columns -> category")
    
    # Print summary
    print(f"\n[RESULT] Final shape: {df.shape}")
    memory_mb = df.memory_usage(deep=True).sum() / 1024**2
    print(f"[RESULT] Memory usage: {memory_mb:.2f} MB")
    print("="*70 + "\n")
    
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
        metric (str): One of get_available_metrics()
    
    Returns:
        dict: {'metric_value': float (0-100), 'respondents': int}
              Returns {'metric_value': 0.0, 'respondents': 0} if country not found
    
    Example:
        >>> result = get_country_metric_value(df_clean, 'United States', 'treatment_rate')
        >>> print(f"Treatment rate in US: {result['metric_value']}% ({result['respondents']} respondents)")
        Treatment rate in US: 50.2% (1234 respondents)
    """
    choropleth_df = get_choropleth_data(df, metric)
    country_row = choropleth_df[choropleth_df['Country'] == country]
    
    if country_row.empty:
        return {'metric_value': 0.0, 'respondents': 0}
    
    return {
        'metric_value': country_row['metric_value'].values[0],
        'respondents': country_row['respondents'].values[0]
    }


if __name__ == "__main__":
    # Run analysis when script is executed directly
    report = analyze_data_quality()
    print_quality_report(report)
