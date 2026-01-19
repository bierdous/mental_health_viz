"""
Demo script for butterfly chart data aggregation function.

Displays output of get_butterfly_data() function for single and dual country comparisons.
Verifies that percentages sum to 100% for each employment status.

Run: python tests/test_butterfly.py
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from preprocessing import (
    clean_and_convert_types,
    get_butterfly_data
)


def main():
    """Run butterfly chart demo."""
    print("\n" + "="*80)
    print("BUTTERFLY CHART DATA AGGREGATION - DEMO")
    print("="*80)
    
    # Load and clean data
    print("\n[LOADING DATA]")
    df = clean_and_convert_types()
    
    # Demo 1: Single country
    print("\n" + "="*80)
    print("DEMO 1: SINGLE COUNTRY BUTTERFLY DATA")
    print("="*80)
    
    country1 = 'United States'
    butterfly_data = get_butterfly_data(df, country1)
    
    print(f"\nCountry: {country1}")
    print(f"Days Indoors Categories: {', '.join(butterfly_data['days_indoors_order'])}")
    
    print(f"\n[EMPLOYED] (self_employed = No):")
    employed_values = butterfly_data['country1']['employed'].values()
    employed_sum = sum(employed_values)
    for day_cat, pct in butterfly_data['country1']['employed'].items():
        print(f"  {day_cat:<20s}: {pct:>6.2f}%")
    print(f"  {'Total':<20s}: {employed_sum:>6.2f}%")
    
    print(f"\n[SELF-EMPLOYED] (self_employed = Yes):")
    self_emp_values = butterfly_data['country1']['self_employed'].values()
    self_emp_sum = sum(self_emp_values)
    for day_cat, pct in butterfly_data['country1']['self_employed'].items():
        print(f"  {day_cat:<20s}: {pct:>6.2f}%")
    print(f"  {'Total':<20s}: {self_emp_sum:>6.2f}%")
    
    # Verify sums
    print(f"\n[VERIFICATION]")
    employed_check = "✓ PASS" if abs(employed_sum - 100.0) < 0.01 else "✗ FAIL"
    self_emp_check = "✓ PASS" if abs(self_emp_sum - 100.0) < 0.01 else "✗ FAIL"
    print(f"  Employed percentages sum to 100%: {employed_check}")
    print(f"  Self-Employed percentages sum to 100%: {self_emp_check}")
    
    # Demo 2: Two countries comparison
    print("\n" + "="*80)
    print("DEMO 2: TWO COUNTRIES BUTTERFLY COMPARISON")
    print("="*80)
    
    country1 = 'United States'
    country2 = 'India'
    butterfly_data = get_butterfly_data(df, country1, country2)
    
    print(f"\nComparing: {country1} vs {country2}\n")
    
    # Country 1
    print(f">>> {country1}")
    print(f"\n    [EMPLOYED] (self_employed = No):")
    employed_sums = {'country1': 0.0, 'country2': 0.0}
    for day_cat in butterfly_data['days_indoors_order']:
        val1 = butterfly_data['country1']['employed'][day_cat]
        employed_sums['country1'] += val1
        print(f"      {day_cat:<20s}: {val1:>6.2f}%")
    print(f"      {'TOTAL':<20s}: {employed_sums['country1']:>6.2f}%")
    
    print(f"\n    [SELF-EMPLOYED] (self_employed = Yes):")
    self_emp_sums = {'country1': 0.0, 'country2': 0.0}
    for day_cat in butterfly_data['days_indoors_order']:
        val1 = butterfly_data['country1']['self_employed'][day_cat]
        self_emp_sums['country1'] += val1
        print(f"      {day_cat:<20s}: {val1:>6.2f}%")
    print(f"      {'TOTAL':<20s}: {self_emp_sums['country1']:>6.2f}%")
    
    # Country 2
    print(f"\n>>> {country2}")
    print(f"\n    [EMPLOYED] (self_employed = No):")
    for day_cat in butterfly_data['days_indoors_order']:
        val2 = butterfly_data['country2']['employed'][day_cat]
        employed_sums['country2'] += val2
        print(f"      {day_cat:<20s}: {val2:>6.2f}%")
    print(f"      {'TOTAL':<20s}: {employed_sums['country2']:>6.2f}%")
    
    print(f"\n    [SELF-EMPLOYED] (self_employed = Yes):")
    for day_cat in butterfly_data['days_indoors_order']:
        val2 = butterfly_data['country2']['self_employed'][day_cat]
        self_emp_sums['country2'] += val2
        print(f"      {day_cat:<20s}: {val2:>6.2f}%")
    print(f"      {'TOTAL':<20s}: {self_emp_sums['country2']:>6.2f}%")
    
    # Verify all sums
    print(f"\n[VERIFICATION]")
    all_pass = True
    for country_label, country_key in [(country1, 'country1'), (country2, 'country2')]:
        emp_check = "✓ PASS" if abs(employed_sums[country_key] - 100.0) < 0.01 else "✗ FAIL"
        self_emp_check = "✓ PASS" if abs(self_emp_sums[country_key] - 100.0) < 0.01 else "✗ FAIL"
        all_pass = all_pass and (abs(employed_sums[country_key] - 100.0) < 0.01 and abs(self_emp_sums[country_key] - 100.0) < 0.01)
        print(f"  {country_label:<25s} - Employed: {emp_check} | Self-Employed: {self_emp_check}")
    
    # Demo 3: Multiple country pairs
    print("\n" + "="*80)
    print("DEMO 3: MULTIPLE COUNTRIES - PERCENTAGE VERIFICATION")
    print("="*80)
    
    test_countries = [
        'United States',
        'United Kingdom',
        'Germany',
        'India',
        'Brazil',
        'Australia'
    ]
    
    all_valid = True
    for country in test_countries:
        butterfly_data = get_butterfly_data(df, country)
        
        employed_total = sum(butterfly_data['country1']['employed'].values())
        self_emp_total = sum(butterfly_data['country1']['self_employed'].values())
        
        employed_valid = abs(employed_total - 100.0) < 0.01
        self_emp_valid = abs(self_emp_total - 100.0) < 0.01
        
        status = "✓" if (employed_valid and self_emp_valid) else "✗"
        all_valid = all_valid and employed_valid and self_emp_valid
        
        print(f"{status} {country:<25s} | Employed: {employed_total:>7.2f}% | Self-Emp: {self_emp_total:>7.2f}%")
    
    print("\n" + "="*80)
    if all_valid:
        print("DEMO COMPLETE - ALL VERIFICATION CHECKS PASSED ✓")
    else:
        print("DEMO COMPLETE - SOME VERIFICATION CHECKS FAILED ✗")
    print("="*80 + "\n")


if __name__ == '__main__':
    main()
