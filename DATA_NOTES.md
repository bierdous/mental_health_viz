# Data Processing Notes

## Dataset: mental_dataset.csv

### Original Data Quality
- **Total Records**: 292,364 rows
- **Total Columns**: 17
- **Date Range**: August 27, 2014 to February 1, 2016 (~1.5 years)
- **Geographic Coverage**: 35 countries

### Handling of Missing Data

#### `self_employed` Column
- **Original Missing Count**: 5,202 rows (1.78%)
- **Handling Method**: **Filled with 'Unknown' category**
- **Rationale**: 
  - Preserves all records for analysis (no data loss)
  - Makes uncertainty visible in visualizations
  - Allows filtering/analysis of uncertain employment status
  - Typical for survey data where some respondents skip questions

## Notes for Contributors

- The `Unknown` category in `self_employed` should be **visible** in dashboards so users understand data limitations
- When filtering by `self_employed`, include 'Unknown' in filters unless specifically analyzing only Yes/No
- Categorical types are **memory-efficient** but require `.cat.codes` for numeric operations
- `Mood_Swings` uses Low/Medium/High, not Yes/No/Maybe like other survey columns
- `mental_health_interview` and `care_options` have skewed distributions (80% "No", 40% "No" respectively) - useful for segmentation
