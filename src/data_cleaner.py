"""
data_cleaner.py

Purpose:
    Clean the raw bank loan dataset: handle missing values, remove
    duplicates, fix data types, and flag outliers using the IQR method.
    Saves the cleaned dataset to data/processed/.

Author: (your name)
"""

import os
import pandas as pd
import numpy as np


# Columns we expect to be numeric. Defined once here so both the
# type-fixing and outlier-detection functions can reuse this list.
NUMERIC_COLUMNS = [
    "person_age",
    "person_income",
    "person_emp_exp",
    "loan_amnt",
    "loan_int_rate",
    "loan_percent_income",
    "cb_person_cred_hist_length",
    "credit_score",
]

# Columns we expect to be categorical (text/labels).
CATEGORICAL_COLUMNS = [
    "person_gender",
    "person_education",
    "person_home_ownership",
    "loan_intent",
    "previous_loan_defaults_on_file",
]


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Fill missing values: numeric columns get the median (robust to
    outliers/skew), categorical columns get the mode (most frequent value).

    Parameters
    ----------
    df : pd.DataFrame

    Returns
    -------
    pd.DataFrame
        DataFrame with missing values filled.
    """
    df = df.copy()  # never mutate the caller's original DataFrame

    for col in NUMERIC_COLUMNS:
        if col in df.columns and df[col].isnull().sum() > 0:
            median_value = df[col].median()
            df[col] = df[col].fillna(median_value)
            print(f"Filled missing values in '{col}' with median: {median_value}")

    for col in CATEGORICAL_COLUMNS:
        if col in df.columns and df[col].isnull().sum() > 0:
            mode_value = df[col].mode()[0]
            df[col] = df[col].fillna(mode_value)
            print(f"Filled missing values in '{col}' with mode: {mode_value}")

    return df


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove fully duplicated rows from the DataFrame.

    Parameters
    ----------
    df : pd.DataFrame

    Returns
    -------
    pd.DataFrame
        DataFrame with duplicate rows removed.
    """
    df = df.copy()
    before = len(df)
    df = df.drop_duplicates()
    after = len(df)
    print(f"Removed {before - after} duplicate rows ({before} -> {after} rows).")
    return df


def fix_data_types(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ensure numeric columns are numeric and categorical columns are
    proper string/category dtype.

    Parameters
    ----------
    df : pd.DataFrame

    Returns
    -------
    pd.DataFrame
        DataFrame with corrected data types.
    """
    df = df.copy()

    for col in NUMERIC_COLUMNS:
        if col in df.columns:
            # errors="coerce" turns any unparseable value into NaN
            # instead of crashing the whole pipeline.
            df[col] = pd.to_numeric(df[col], errors="coerce")

    for col in CATEGORICAL_COLUMNS:
        if col in df.columns:
            df[col] = df[col].astype("category")

    # loan_status is our binary target: 1 = repaid, 0 = defaulted
    if "loan_status" in df.columns:
        df["loan_status"] = df["loan_status"].astype(int)

    print("Data types fixed for numeric and categorical columns.")
    return df


def detect_outliers_iqr(df: pd.DataFrame, column: str) -> pd.Series:
    """
    Detect outliers in a numeric column using the IQR (Interquartile
    Range) method. Returns a boolean Series: True where the row is
    an outlier for this column.

    Parameters
    ----------
    df : pd.DataFrame
    column : str
        Name of the numeric column to check.

    Returns
    -------
    pd.Series
        Boolean mask, True = outlier row.
    """
    q1 = df[column].quantile(0.25)
    q3 = df[column].quantile(0.75)
    iqr = q3 - q1

    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    return (df[column] < lower_bound) | (df[column] > upper_bound)


def flag_outliers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add a boolean flag column for each key numeric field indicating
    whether that row is an outlier, plus one summary column
    'is_any_outlier'. We FLAG rather than delete, since outliers in
    income/loan amount may represent real, important risk cases.

    Parameters
    ----------
    df : pd.DataFrame

    Returns
    -------
    pd.DataFrame
        DataFrame with added outlier flag columns.
    """
    df = df.copy()

    # Focus outlier detection on the columns most relevant to risk analysis.
    columns_to_check = ["person_income", "loan_amnt", "person_age"]

    outlier_flags = pd.DataFrame(index=df.index)
    for col in columns_to_check:
        if col in df.columns:
            flag_col = f"{col}_is_outlier"
            outlier_flags[flag_col] = detect_outliers_iqr(df, col)
            df[flag_col] = outlier_flags[flag_col]
            count = outlier_flags[flag_col].sum()
            print(f"Outliers detected in '{col}': {count} rows")

    # A row is flagged 'is_any_outlier' if it's an outlier in ANY checked column
    df["is_any_outlier"] = outlier_flags.any(axis=1)

    return df


def clean_pipeline(df: pd.DataFrame) -> pd.DataFrame:
    """
    Run the full cleaning pipeline in order: missing values -> duplicates
    -> data types -> outlier flagging.

    Parameters
    ----------
    df : pd.DataFrame
        Raw DataFrame.

    Returns
    -------
    pd.DataFrame
        Fully cleaned DataFrame, ready for analysis.
    """
    print("\n--- Starting cleaning pipeline ---")
    df = handle_missing_values(df)
    df = remove_duplicates(df)
    df = fix_data_types(df)
    df = flag_outliers(df)
    print("--- Cleaning pipeline complete ---\n")
    return df


def save_processed_data(df: pd.DataFrame, output_path: str) -> None:
    """
    Save the cleaned DataFrame to the processed data folder.

    Parameters
    ----------
    df : pd.DataFrame
    output_path : str
        Destination path, e.g. 'data/processed/loan_data_cleaned.csv'
    """
    # Ensure the destination folder exists before writing.
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"✅ Cleaned dataset saved to: {output_path}")


if __name__ == "__main__":
    # Import here (not at top) to avoid circular import issues when
    # this file is imported elsewhere as a module.
    from data_loader import load_raw_data

    RAW_PATH = os.path.join("data", "raw", "loan_data.csv")
    PROCESSED_PATH = os.path.join("data", "processed", "loan_data_cleaned.csv")

    raw_df = load_raw_data(RAW_PATH)
    cleaned_df = clean_pipeline(raw_df)
    save_processed_data(cleaned_df, PROCESSED_PATH)