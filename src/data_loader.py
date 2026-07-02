"""
data_loader.py

Purpose:
    Load the raw bank loan dataset from disk into a pandas DataFrame,
    with basic file-existence checks and load confirmation logging.

Author: (your name)
"""

import os
import pandas as pd


def load_raw_data(file_path: str) -> pd.DataFrame:
    """
    Load the raw loan dataset CSV into a pandas DataFrame.

    Parameters
    ----------
    file_path : str
        Path to the raw CSV file (e.g., 'data/raw/loan_data.csv').

    Returns
    -------
    pd.DataFrame
        The loaded dataset as a DataFrame.

    Raises
    ------
    FileNotFoundError
        If the given file_path does not exist.
    """
    # Check the file actually exists before trying to read it.
    # This gives a clear, friendly error instead of a confusing pandas traceback.
    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"Could not find dataset at: {file_path}. "
            f"Make sure the CSV is placed in data/raw/."
        )

    # Read the CSV into a DataFrame.
    df = pd.read_csv(file_path)

    # Print a quick confirmation so we know loading succeeded, and
    # get an immediate sense of the dataset's size.
    print(f"✅ Dataset loaded successfully from: {file_path}")
    print(f"   Shape: {df.shape[0]} rows, {df.shape[1]} columns")

    return df


def inspect_data(df: pd.DataFrame) -> None:
    """
    Print a structured inspection summary of the DataFrame:
    shape, column names, data types, missing values, and a preview.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame to inspect.
    """
    print("\n" + "=" * 60)
    print("DATASET INSPECTION SUMMARY")
    print("=" * 60)

    # Basic shape info
    print(f"\nShape: {df.shape[0]} rows x {df.shape[1]} columns")

    # Column names and their data types
    print("\nColumn Data Types:")
    print(df.dtypes)

    # Count of missing values per column
    print("\nMissing Values per Column:")
    missing = df.isnull().sum()
    print(missing[missing > 0] if missing.sum() > 0 else "No missing values found.")

    # Number of fully duplicated rows
    print(f"\nDuplicate Rows: {df.duplicated().sum()}")

    # Preview first 5 rows
    print("\nFirst 5 Rows Preview:")
    print(df.head())

    print("=" * 60 + "\n")


# This block only runs if you execute this file directly
# (e.g., `python src/data_loader.py`), not when it's imported elsewhere.
# It's useful for quickly testing this module on its own.
if __name__ == "__main__":
    RAW_DATA_PATH = os.path.join("data", "raw", "loan_data.csv")
    data = load_raw_data(RAW_DATA_PATH)
    inspect_data(data)