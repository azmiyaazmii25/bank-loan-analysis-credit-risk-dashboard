"""
main.py

Purpose:
    Orchestrates the full Bank Loan Analysis & Credit Risk Assessment
    pipeline end-to-end: load raw data -> clean it -> run EDA ->
    generate charts. Run this file to execute the entire project
    with a single command.

Usage:
    python main.py

Author: (your name)
"""

import os
import sys

# Ensure the src/ folder is importable as a package from the project root.
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from data_loader import load_raw_data, inspect_data
from data_cleaner import clean_pipeline, save_processed_data
from eda_analysis import load_processed_data, run_full_eda
from visualization import generate_all_charts


# Centralized file paths, defined once so every step agrees on locations.
RAW_DATA_PATH = os.path.join("data", "raw", "loan_data.csv")
PROCESSED_DATA_PATH = os.path.join("data", "processed", "loan_data_cleaned.csv")


def run_pipeline() -> None:
    """
    Execute the full pipeline in order:
    1. Load raw data
    2. Inspect it
    3. Clean it
    4. Save the cleaned version
    5. Run full EDA
    6. Generate all charts
    """
    print("=" * 60)
    print("BANK LOAN ANALYSIS & CREDIT RISK ASSESSMENT PIPELINE")
    print("=" * 60)

    # Step 1: Load raw data
    raw_df = load_raw_data(RAW_DATA_PATH)

    # Step 2: Inspect it (prints structure, missing values, duplicates)
    inspect_data(raw_df)

    # Step 3: Clean it (missing values, duplicates, dtypes, outlier flags)
    cleaned_df = clean_pipeline(raw_df)

    # Step 4: Save cleaned dataset to data/processed/
    save_processed_data(cleaned_df, PROCESSED_DATA_PATH)

    # Step 5: Run full exploratory data analysis
    processed_df = load_processed_data(PROCESSED_DATA_PATH)
    run_full_eda(processed_df)

    # Step 6: Generate and save all charts
    generate_all_charts(processed_df)

    print("=" * 60)
    print("✅ PIPELINE COMPLETE")
    print(f"   Cleaned data: {PROCESSED_DATA_PATH}")
    print(f"   Charts saved: outputs/charts/")
    print("=" * 60)


if __name__ == "__main__":
    try:
        run_pipeline()
    except FileNotFoundError as e:
        print(f"\n❌ Pipeline stopped: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error during pipeline execution: {e}")
        sys.exit(1)