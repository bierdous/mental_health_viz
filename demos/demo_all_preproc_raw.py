"""
Raw dictionary output from all graph preprocessing functions.

Shows the exact structure of each function's return value.

Run: python tests/test_all_graphs.py
"""

import sys
from pathlib import Path
import json

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from preprocessing import (
    clean_and_convert_types,
    get_country_metric_value,
    get_radar_data,
    get_butterfly_data,
    get_stacked_bar_data
)


def main():
    """Output raw dictionaries from all preprocessing functions."""
    df = clean_and_convert_types()
    
    print("\n" + "="*80)
    print("RAW DICTIONARY OUTPUT - ALL FUNCTIONS")
    print("="*80)
    
    # 1. get_country_metric_value
    print("\n[1] get_country_metric_value(df, 'United States', 'treatment_rate')")
    result = get_country_metric_value(df, 'United States', 'treatment_rate')
    print(json.dumps(result, indent=2))
    
    # 2. get_radar_data - single country
    print("\n[2] get_radar_data(df, 'United States')")
    result = get_radar_data(df, 'United States')
    print(json.dumps(result, indent=2))
    
    # 3. get_radar_data - two countries
    print("\n[3] get_radar_data(df, 'United States', 'India')")
    result = get_radar_data(df, 'United States', 'India')
    print(json.dumps(result, indent=2))
    
    # 4. get_butterfly_data - single country
    print("\n[4] get_butterfly_data(df, 'United States')")
    result = get_butterfly_data(df, 'United States')
    print(json.dumps(result, indent=2))
    
    # 5. get_butterfly_data - two countries
    print("\n[5] get_butterfly_data(df, 'United States', 'India')")
    result = get_butterfly_data(df, 'United States', 'India')
    print(json.dumps(result, indent=2))
    
    # 6. get_stacked_bar_data - single country
    print("\n[6] get_stacked_bar_data(df, 'United States')")
    result = get_stacked_bar_data(df, 'United States')
    print(json.dumps(result, indent=2))
    
    # 7. get_stacked_bar_data - two countries
    print("\n[7] get_stacked_bar_data(df, 'United States', 'India')")
    result = get_stacked_bar_data(df, 'United States', 'India')
    print(json.dumps(result, indent=2))
    
    print("\n" + "="*80 + "\n")


if __name__ == '__main__':
    main()
