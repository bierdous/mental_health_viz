"""
Demo script for choropleth data aggregation functions.

Displays output of preprocessing functions:
- get_available_metrics()
- get_choropleth_data()
- get_country_metric_value()

Run: python tests/test_choropleth.py
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from preprocessing import (
    clean_and_convert_types,
    get_available_metrics,
    get_choropleth_data,
    get_country_metric_value,
    print_categorical_columns
)


def main():
    """Run choropleth demo."""
    print("\n" + "="*80)
    print("CHOROPLETH DATA AGGREGATION - DEMO")
    print("="*80)
    
    # Load and clean data
    print("\n[LOADING DATA]")
    df = clean_and_convert_types()
    
    # Print categorical columns
    print_categorical_columns(df)
    
    # Get available metrics
    print("\n[AVAILABLE METRICS]")
    print("-" * 80)
    metrics_dict = get_available_metrics()
    metrics = list(metrics_dict.keys())
    for i, metric in enumerate(metrics, 1):
        print(f"{i}. {metric}")
    
    # Display data for each metric
    print("\n[CHOROPLETH DATA BY METRIC]")
    print("-" * 80)
    
    for metric in metrics:
        print(f"\n>>> {metric}")
        print("   " + "-" * 76)
        
        result = get_choropleth_data(df, metric)
        
        # Statistics
        min_val = result['metric_value'].min()
        max_val = result['metric_value'].max()
        mean_val = result['metric_value'].mean()
        
        print(f"   Countries: {len(result)}")
        print(f"   Range: {min_val:.2f}% - {max_val:.2f}%")
        print(f"   Mean: {mean_val:.2f}%")
        
        # Top 5 countries
        print(f"\n   Top 5 countries:")
        for rank, (_, row) in enumerate(result.nlargest(5, 'metric_value').iterrows(), 1):
            print(f"      {rank:2d}. {row['Country']:25s} {row['metric_value']:6.2f}% (n={row['respondents']:,})")
        
        # Bottom 5 countries
        print(f"\n   Bottom 5 countries:")
        for rank, (_, row) in enumerate(result.nsmallest(5, 'metric_value').iterrows(), 1):
            print(f"      {rank:2d}. {row['Country']:25s} {row['metric_value']:6.2f}% (n={row['respondents']:,})")
    
    # Country lookups
    print("\n[COUNTRY METRIC LOOKUPS]")
    print("-" * 80)
    
    sample_countries = ['United States', 'United Kingdom', 'Germany', 'India', 'Brazil']
    sample_metrics = metrics[:3]  # First 3 metrics
    
    print(f"\nLookup table for {len(sample_countries)} countries × {len(sample_metrics)} metrics:\n")
    
    # Header
    header = f"{'Country':<20}"
    for metric in sample_metrics:
        header += f" | {metric:<25}"
    print(header)
    print("-" * (len(header)))
    
    # Data rows
    for country in sample_countries:
        row = f"{country:<20}"
        for metric in sample_metrics:
            result = get_country_metric_value(df, country, metric)
            value = result['metric_value']
            respondents = result['respondents']
            row += f" | {value:>6.2f}% (n={respondents:>5,})"
        print(row)
    
    print("\n" + "="*80)
    print("DEMO COMPLETE")
    print("="*80 + "\n")


if __name__ == '__main__':
    main()

