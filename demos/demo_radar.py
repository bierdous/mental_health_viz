"""
Demo script for radar chart data aggregation function.

Displays output of get_radar_data() function for single and dual country comparisons.

Run: python tests/test_radar.py
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from preprocessing import (
    clean_and_convert_types,
    get_radar_data
)


def main():
    """Run radar chart demo."""
    print("\n" + "="*80)
    print("RADAR CHART DATA AGGREGATION - DEMO")
    print("="*80)
    
    # Load and clean data
    print("\n[LOADING DATA]")
    df = clean_and_convert_types()
    
     # Filter to country data
    test_df = df[df['Country'] == "Germany"]
    
    # Calculate metric for this country only
    count_yes = (test_df["Coping_Struggles"] == "Yes").sum()
    total = len(test_df)
    percentage = (count_yes / total * 100) if total > 0 else 0
    print(percentage)
    # Demo 1: Single country
    print("\n" + "="*80)
    print("DEMO 1: SINGLE COUNTRY RADAR DATA")
    print("="*80)
    
    country1 = 'United States'
    radar_data = get_radar_data(df, country1)
    
    print(f"\nCountry: {country1}")
    print(f"Metrics: {', '.join(radar_data['metrics'])}")
    print(f"\nRadar values:")
    for metric, value in zip(radar_data['metrics'], radar_data['country1']['values']):
        print(f"  {metric:<20s}: {value:>6.2f}%")
    
    # Demo 2: Two countries comparison
    print("\n" + "="*80)
    print("DEMO 2: TWO COUNTRIES OVERLAY COMPARISON")
    print("="*80)
    
    country1 = 'United States'
    country2 = 'India'
    radar_data = get_radar_data(df, country1, country2)
    
    print(f"\nComparing: {country1} vs {country2}")
    print(f"Metrics: {', '.join(radar_data['metrics'])}")
    
    print(f"\n{country1:<30s} | {country2:<30s}")
    print("-" * 65)
    for metric, val1, val2 in zip(radar_data['metrics'], 
                                   radar_data['country1']['values'], 
                                   radar_data['country2']['values']):
        diff = val1 - val2
        diff_marker = "↑" if diff > 0 else "↓" if diff < 0 else "="
        print(f"{metric:<20s} {val1:>6.2f}% | {val2:>6.2f}% {diff_marker} ({diff:+.2f}%)")
    
    # Demo 3: Multiple country pairs
    print("\n" + "="*80)
    print("DEMO 3: MULTIPLE COUNTRY COMPARISONS")
    print("="*80)
    
    country_pairs = [
        ('United States', 'United Kingdom'),
        ('Germany', 'France'),
        ('Australia', 'New Zealand'),
    ]
    
    for country1, country2 in country_pairs:
        radar_data = get_radar_data(df, country1, country2)
        
        print(f"\n>>> {country1} vs {country2}")
        print("   " + "-" * 60)
        
        for metric, val1, val2 in zip(radar_data['metrics'],
                                       radar_data['country1']['values'],
                                       radar_data['country2']['values']):
            diff = val1 - val2
            print(f"   {metric:<20s}: {val1:>6.2f}% | {val2:>6.2f}% (diff: {diff:+.2f}%)")
    
    print("\n" + "="*80)
    print("DEMO COMPLETE")
    print("="*80 + "\n")


if __name__ == '__main__':
    main()
