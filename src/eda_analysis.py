"""
eda_analysis.py

Purpose:
    Perform exploratory data analysis on the cleaned loan dataset:
    approval/rejection rates, income, gender, loan intent (occupation
    proxy), credit score/history, loan amount, default rate, risk,
    and correlation analysis. Each function prints a summary and
    returns the underlying data for reuse in visualization.py.

Author: (your name)
"""

import os
import pandas as pd
import numpy as np


def load_processed_data(file_path: str) -> pd.DataFrame:
    """Load the cleaned dataset produced by data_cleaner.py."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Processed dataset not found at: {file_path}")
    df = pd.read_csv(file_path)
    print(f"✅ Processed dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    return df


def approval_rejection_analysis(df: pd.DataFrame) -> pd.Series:
    """
    Analyze loan approval vs rejection counts and rates.
    Note: 'loan_status' here means 1 = repaid/approved-and-good,
    0 = defaulted. We treat it as our approval/outcome proxy.
    """
    counts = df["loan_status"].value_counts()
    rate = df["loan_status"].value_counts(normalize=True) * 100

    print("\n--- Loan Status Analysis ---")
    print(f"Approved/Good (1): {counts.get(1, 0)} ({rate.get(1, 0):.2f}%)")
    print(f"Defaulted/Bad (0): {counts.get(0, 0)} ({rate.get(0, 0):.2f}%)")

    return counts


def income_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Analyze income distribution overall and by loan status."""
    summary = df.groupby("loan_status")["person_income"].describe()
    print("\n--- Income Analysis by Loan Status ---")
    print(summary)
    return summary


def gender_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Analyze loan status outcomes broken down by gender."""
    summary = pd.crosstab(df["person_gender"], df["loan_status"], normalize="index") * 100
    print("\n--- Gender vs Loan Status (%) ---")
    print(summary.round(2))
    return summary


def loan_intent_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """
    Analyze loan status by loan_intent (used as an 'occupation/purpose'
    proxy, since this dataset has no direct occupation column).
    """
    summary = pd.crosstab(df["loan_intent"], df["loan_status"], normalize="index") * 100
    print("\n--- Loan Intent vs Loan Status (%) ---")
    print(summary.round(2))
    return summary


def credit_score_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Analyze credit score distribution by loan status."""
    summary = df.groupby("loan_status")["credit_score"].describe()
    print("\n--- Credit Score Analysis by Loan Status ---")
    print(summary)
    return summary


def credit_history_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Analyze credit history length vs loan status."""
    summary = df.groupby("loan_status")["cb_person_cred_hist_length"].describe()
    print("\n--- Credit History Length by Loan Status ---")
    print(summary)
    return summary


def loan_amount_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Analyze loan amount distribution by loan status."""
    summary = df.groupby("loan_status")["loan_amnt"].describe()
    print("\n--- Loan Amount Analysis by Loan Status ---")
    print(summary)
    return summary


def default_rate_analysis(df: pd.DataFrame) -> pd.Series:
    """
    Calculate default rate (loan_status == 0) segmented by
    previous_loan_defaults_on_file, to see if past defaults predict
    future ones.
    """
    default_rate = (
        df.groupby("previous_loan_defaults_on_file")["loan_status"]
        .apply(lambda x: (x == 0).mean() * 100)
    )
    print("\n--- Default Rate (%) by Previous Default History ---")
    print(default_rate.round(2))
    return default_rate


def risk_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """
    Build a simple composite risk view: average credit score, income,
    and default rate, segmented by home ownership status.
    """
    risk_summary = df.groupby("person_home_ownership").agg(
        avg_credit_score=("credit_score", "mean"),
        avg_income=("person_income", "mean"),
        default_rate_pct=("loan_status", lambda x: (x == 0).mean() * 100),
    ).round(2)

    print("\n--- Risk Profile by Home Ownership ---")
    print(risk_summary)
    return risk_summary


def correlation_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Compute correlation matrix for key numeric risk factors."""
    numeric_cols = [
        "person_age", "person_income", "person_emp_exp",
        "loan_amnt", "loan_int_rate", "loan_percent_income",
        "cb_person_cred_hist_length", "credit_score", "loan_status",
    ]
    corr_matrix = df[numeric_cols].corr()
    print("\n--- Correlation Matrix (Key Numeric Fields) ---")
    print(corr_matrix.round(2))
    return corr_matrix


def statistical_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Full descriptive statistics for all numeric columns."""
    summary = df.describe().round(2)
    print("\n--- Full Statistical Summary ---")
    print(summary)
    return summary


def run_full_eda(df: pd.DataFrame) -> dict:
    """
    Run every EDA function in sequence and collect results into a
    dictionary, so main.py or a notebook can access any result by name.
    """
    results = {
        "approval_rejection": approval_rejection_analysis(df),
        "income": income_analysis(df),
        "gender": gender_analysis(df),
        "loan_intent": loan_intent_analysis(df),
        "credit_score": credit_score_analysis(df),
        "credit_history": credit_history_analysis(df),
        "loan_amount": loan_amount_analysis(df),
        "default_rate": default_rate_analysis(df),
        "risk": risk_analysis(df),
        "correlation": correlation_analysis(df),
        "statistical_summary": statistical_summary(df),
    }
    return results


if __name__ == "__main__":
    PROCESSED_PATH = os.path.join("data", "processed", "loan_data_cleaned.csv")
    data = load_processed_data(PROCESSED_PATH)
    run_full_eda(data)