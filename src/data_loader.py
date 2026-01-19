import pandas as pd
import os
from pathlib import Path

# Cache for the dataframe
_df_cache = None


def get_data(filepath="data/mental_dataset.csv"):
    """
    Load mental health dataset from CSV file with caching.
    
    Args:
        filepath (str): Path to the CSV file (relative to project root)
    
    Returns:
        pd.DataFrame: Loaded dataset
    
    Raises:
        FileNotFoundError: If the CSV file doesn't exist
        pd.errors.ParserError: If the CSV is malformed
    """
    global _df_cache
    
    # Return cached data if already loaded
    if _df_cache is not None:
        return _df_cache
    
    # Resolve path relative to project root
    project_root = Path(__file__).parent.parent
    full_path = project_root / filepath
    
    # Check if file exists
    if not full_path.exists():
        raise FileNotFoundError(f"Dataset not found at {full_path}")
    
    # Load CSV
    try:
        _df_cache = pd.read_csv(full_path)
        print(f"[OK] Loaded dataset: {len(_df_cache)} rows, {len(_df_cache.columns)} columns")
        return _df_cache
    except pd.errors.ParserError as e:
        raise pd.errors.ParserError(f"Failed to parse CSV file: {e}")


def clear_cache():
    """Clear the cached dataframe (useful for testing)."""
    global _df_cache
    _df_cache = None
