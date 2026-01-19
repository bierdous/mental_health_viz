"""
Demo script for stacked bar chart data aggregation function.

Displays output of get_stacked_bar_data() function for single and dual country comparisons.
Verifies that percentages sum to 100% for each interview response category.

Run: python tests/test_stacked_bar.py
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from preprocessing import (
    clean_and_convert_types,
    get_stacked_bar_data
)


def main():
    """Run stacked bar chart demo."""
    print("\n" + "="*80)
    print("STACKED BAR CHART DATA AGGREGATION - DEMO")
    print("="*80)
    
    # Load and clean data
    print("\n[LOADING DATA]")
    df = clean_and_convert_types()
    
    # Demo 1: Single country
    print("\n" + "="*80)
    print("DEMO 1: SINGLE COUNTRY STACKED BAR DATA")
    print("="*80)
    
    country1 = 'United States'
    stacked_data = get_stacked_bar_data(df, country1)
    
    print(f"\nCountry: {country1}")
    print(f"Social Weakness Categories: {', '.join(stacked_data['social_weakness_order'])}")
    print(f"Interview Responses: {', '.join(stacked_data['interview_responses'])}")
    
    print(f"\n[SOCIAL WEAKNESS DISTRIBUTION BY MENTAL HEALTH INTERVIEW RESPONSE]")
    print("-" * 80)
    
    for response in stacked_data['interview_responses']:
        print(f"\nMental Health Interview: {response}")
        weaknesses = stacked_data['country1'][response]
        total = sum(weaknesses.values())
        
        for weakness_cat, pct in weaknesses.items():
            print(f"  {weakness_cat:<15s}: {pct:>6.2f}%")
        print(f"  {'Total':<15s}: {total:>6.2f}%")
        
        # Verify sum
        check = "✓ PASS" if abs(total - 100.0) < 0.01 else "✗ FAIL"
        print(f"  Verification: {check}")
    
    # Demo 2: Two countries comparison
    print("\n" + "="*80)
    print("DEMO 2: TWO COUNTRIES STACKED BAR COMPARISON")
    print("="*80)
    
    country1 = 'United States'
    country2 = 'India'
    stacked_data = get_stacked_bar_data(df, country1, country2)
    
    print(f"\nComparing: {country1} vs {country2}\n")
    
    for response in stacked_data['interview_responses']:
        print(f">>> Mental Health Interview: {response}")
        print(f"    {country1:<30s} | {country2:<30s}")
        print("    " + "-" * 60)
        
        country1_total = 0.0
        country2_total = 0.0
        
        for weakness_cat in stacked_data['social_weakness_order']:
            val1 = stacked_data['country1'][response][weakness_cat]
            val2 = stacked_data['country2'][response][weakness_cat]
            country1_total += val1
            country2_total += val2
            
            print(f"    {weakness_cat:<20s} {val1:>6.2f}% | {val2:>6.2f}%")
        
        print("    " + "-" * 60)
        print(f"    {'TOTAL':<20s} {country1_total:>6.2f}% | {country2_total:>6.2f}%")
        
        # Verify sums
        check1 = "✓" if abs(country1_total - 100.0) < 0.01 else "✗"
        check2 = "✓" if abs(country2_total - 100.0) < 0.01 else "✗"
        print(f"    Verification: {check1} {check2}\n")
    
    # Demo 3: Multiple countries verification
    print("="*80)
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
    
    print("\nVerifying that all interview response categories sum to 100% for each country:\n")
    
    all_valid = True
    for country in test_countries:
        stacked_data = get_stacked_bar_data(df, country)
        
        country_valid = True
        for response in stacked_data['interview_responses']:
            weaknesses = stacked_data['country1'][response]
            total = sum(weaknesses.values())
            valid = abs(total - 100.0) < 0.01
            country_valid = country_valid and valid
        
        status = "✓" if country_valid else "✗"
        all_valid = all_valid and country_valid
        
        print(f"{status} {country:<25s}")
    
    # Demo 4: Response distribution summary
    print("\n" + "="*80)
    print("DEMO 4: SOCIAL WEAKNESS DISTRIBUTION SUMMARY")
    print("="*80)
    
    country = 'United States'
    stacked_data = get_stacked_bar_data(df, country)
    
    print(f"\nCountry: {country}")
    print(f"\nDistribution of '{', '.join(stacked_data['social_weakness_order'])}' weaknesses:")
    print(f"across Mental Health Interview responses:\n")
    
    # Calculate average distribution across all interview responses
    weakness_averages = {weakness: [] for weakness in stacked_data['social_weakness_order']}
    
    for response in stacked_data['interview_responses']:
        for weakness_cat in stacked_data['social_weakness_order']:
            pct = stacked_data['country1'][response][weakness_cat]
            weakness_averages[weakness_cat].append(pct)
    
    print(f"{'Weakness':<15s} | {'Min':<8s} | {'Avg':<8s} | {'Max':<8s}")
    print("-" * 45)
    
    for weakness_cat in stacked_data['social_weakness_order']:
        values = weakness_averages[weakness_cat]
        min_val = min(values)
        avg_val = sum(values) / len(values)
        max_val = max(values)
        
        print(f"{weakness_cat:<15s} | {min_val:>6.2f}% | {avg_val:>6.2f}% | {max_val:>6.2f}%")
    
    print("\n" + "="*80)
    if all_valid:
        print("DEMO COMPLETE - ALL VERIFICATION CHECKS PASSED ✓")
    else:
        print("DEMO COMPLETE - SOME VERIFICATION CHECKS FAILED ✗")
    print("="*80 + "\n")


if __name__ == '__main__':
    main()
