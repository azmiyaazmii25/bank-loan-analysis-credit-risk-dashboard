"""
visualization.py

Purpose:
    Generate professional Matplotlib/Seaborn charts from the cleaned
    loan dataset and EDA results, saving every chart as a PNG into
    outputs/charts/. Each function corresponds to one business question.

Author: (your name)
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Consistent visual style applied to every chart in this file.
sns.set_theme(style="whitegrid")
PALETTE = "viridis"
FIGSIZE_STANDARD = (8, 5)
FIGSIZE_WIDE = (10, 6)

CHARTS_DIR = os.path.join("outputs", "charts")


def _ensure_charts_dir() -> None:
    """Create the charts output folder if it doesn't already exist."""
    os.makedirs(CHARTS_DIR, exist_ok=True)


def _save_and_close(fig, filename: str) -> None:
    """
    Save a figure to outputs/charts/ and close it to free memory.
    Centralizing this avoids repeating save/close logic in every chart function.
    """
    _ensure_charts_dir()
    path = os.path.join(CHARTS_DIR, filename)
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"✅ Chart saved: {path}")


def plot_approval_distribution(df: pd.DataFrame) -> None:
    """Bar chart: count of approved vs rejected loans."""
    fig, ax = plt.subplots(figsize=FIGSIZE_STANDARD)

    counts = df["loan_status"].value_counts().sort_index()
    labels = ["Rejected (0)", "Approved (1)"]

    sns.barplot(x=labels, y=counts.values, hue=labels, palette=PALETTE, legend=False, ax=ax)
    ax.set_title("Loan Approval vs Rejection Count", fontsize=14, fontweight="bold")
    ax.set_ylabel("Number of Applications")
    ax.set_xlabel("Loan Status")

    # Annotate each bar with its exact count for readability.
    for i, v in enumerate(counts.values):
        ax.text(i, v + 300, str(v), ha="center", fontweight="bold")

    _save_and_close(fig, "01_approval_distribution.png")


def plot_income_by_status(df: pd.DataFrame) -> None:
    """Boxplot: income distribution split by approval status."""
    fig, ax = plt.subplots(figsize=FIGSIZE_STANDARD)

    # Clip extreme outliers just for VISUAL clarity (data itself is untouched).
    plot_df = df[df["person_income"] < df["person_income"].quantile(0.95)]

    sns.boxplot(data=plot_df, x="loan_status", y="person_income", hue="loan_status",
                palette=PALETTE, legend=False, ax=ax)
    ax.set_title("Income Distribution by Loan Status (95th percentile clipped)",
                 fontsize=13, fontweight="bold")
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["Rejected", "Approved"])
    ax.set_xlabel("Loan Status")
    ax.set_ylabel("Annual Income")

    _save_and_close(fig, "02_income_by_status.png")


def plot_gender_approval(df: pd.DataFrame) -> None:
    """Grouped bar chart: approval rate by gender."""
    fig, ax = plt.subplots(figsize=FIGSIZE_STANDARD)

    summary = (pd.crosstab(df["person_gender"], df["loan_status"], normalize="index") * 100)
    summary.columns = ["Rejected %", "Approved %"]

    summary.plot(kind="bar", ax=ax, color=sns.color_palette(PALETTE, 2))
    ax.set_title("Approval Rate by Gender", fontsize=14, fontweight="bold")
    ax.set_ylabel("Percentage (%)")
    ax.set_xlabel("Gender")
    ax.tick_params(axis="x", rotation=0)
    ax.legend(title="")

    _save_and_close(fig, "03_gender_approval.png")


def plot_loan_intent_approval(df: pd.DataFrame) -> None:
    """Horizontal bar chart: approval rate by loan intent (occupation/purpose proxy)."""
    fig, ax = plt.subplots(figsize=FIGSIZE_WIDE)

    summary = (pd.crosstab(df["loan_intent"], df["loan_status"], normalize="index") * 100)
    approved_pct = summary[1].sort_values(ascending=True)

    sns.barplot(x=approved_pct.values, y=approved_pct.index, hue=approved_pct.index,
                palette=PALETTE, legend=False, ax=ax)
    ax.set_title("Approval Rate by Loan Intent", fontsize=14, fontweight="bold")
    ax.set_xlabel("Approval Rate (%)")
    ax.set_ylabel("Loan Intent")

    _save_and_close(fig, "04_loan_intent_approval.png")


def plot_credit_score_distribution(df: pd.DataFrame) -> None:
    """Overlapping histogram: credit score distribution by loan status."""
    fig, ax = plt.subplots(figsize=FIGSIZE_STANDARD)

    sns.histplot(data=df, x="credit_score", hue="loan_status", multiple="layer",
                 palette=PALETTE, alpha=0.5, bins=30, ax=ax)
    ax.set_title("Credit Score Distribution by Loan Status", fontsize=14, fontweight="bold")
    ax.set_xlabel("Credit Score")
    ax.set_ylabel("Number of Applicants")

    _save_and_close(fig, "05_credit_score_distribution.png")


def plot_credit_history_length(df: pd.DataFrame) -> None:
    """Boxplot: credit history length by loan status."""
    fig, ax = plt.subplots(figsize=FIGSIZE_STANDARD)

    sns.boxplot(data=df, x="loan_status", y="cb_person_cred_hist_length",
                hue="loan_status", palette=PALETTE, legend=False, ax=ax)
    ax.set_title("Credit History Length by Loan Status", fontsize=14, fontweight="bold")
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["Rejected", "Approved"])
    ax.set_xlabel("Loan Status")
    ax.set_ylabel("Credit History Length (Years)")

    _save_and_close(fig, "06_credit_history_length.png")


def plot_loan_amount_distribution(df: pd.DataFrame) -> None:
    """Boxplot: loan amount by loan status."""
    fig, ax = plt.subplots(figsize=FIGSIZE_STANDARD)

    sns.boxplot(data=df, x="loan_status", y="loan_amnt", hue="loan_status",
                palette=PALETTE, legend=False, ax=ax)
    ax.set_title("Loan Amount by Loan Status", fontsize=14, fontweight="bold")
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["Rejected", "Approved"])
    ax.set_xlabel("Loan Status")
    ax.set_ylabel("Loan Amount")

    _save_and_close(fig, "07_loan_amount_distribution.png")


def plot_previous_default_impact(df: pd.DataFrame) -> None:
    """Bar chart: rejection rate by previous default history."""
    fig, ax = plt.subplots(figsize=FIGSIZE_STANDARD)

    rejection_rate = (
        df.groupby("previous_loan_defaults_on_file")["loan_status"]
        .apply(lambda x: (x == 0).mean() * 100)
    )

    sns.barplot(x=rejection_rate.index, y=rejection_rate.values,
                hue=rejection_rate.index, palette=PALETTE, legend=False, ax=ax)
    ax.set_title("Rejection Rate by Previous Default History", fontsize=14, fontweight="bold")
    ax.set_xlabel("Previous Loan Defaults on File")
    ax.set_ylabel("Rejection Rate (%)")
    ax.set_ylim(0, 110)

    for i, v in enumerate(rejection_rate.values):
        ax.text(i, v + 2, f"{v:.1f}%", ha="center", fontweight="bold")

    _save_and_close(fig, "08_previous_default_impact.png")


def plot_risk_by_home_ownership(df: pd.DataFrame) -> None:
    """Bar chart: rejection rate segmented by home ownership status."""
    fig, ax = plt.subplots(figsize=FIGSIZE_STANDARD)

    risk = (
        df.groupby("person_home_ownership")["loan_status"]
        .apply(lambda x: (x == 0).mean() * 100)
        .sort_values(ascending=False)
    )

    sns.barplot(x=risk.index, y=risk.values, hue=risk.index,
                palette=PALETTE, legend=False, ax=ax)
    ax.set_title("Rejection Rate by Home Ownership", fontsize=14, fontweight="bold")
    ax.set_xlabel("Home Ownership")
    ax.set_ylabel("Rejection Rate (%)")

    _save_and_close(fig, "09_risk_by_home_ownership.png")


def plot_correlation_heatmap(df: pd.DataFrame) -> None:
    """Heatmap: correlation matrix of key numeric risk factors."""
    fig, ax = plt.subplots(figsize=FIGSIZE_WIDE)

    numeric_cols = [
        "person_age", "person_income", "person_emp_exp",
        "loan_amnt", "loan_int_rate", "loan_percent_income",
        "cb_person_cred_hist_length", "credit_score", "loan_status",
    ]
    corr = df[numeric_cols].corr()

    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", center=0,
                square=True, linewidths=0.5, ax=ax)
    ax.set_title("Correlation Matrix — Key Risk Factors", fontsize=14, fontweight="bold")

    _save_and_close(fig, "10_correlation_heatmap.png")


def plot_loan_percent_income_impact(df: pd.DataFrame) -> None:
    """
    Boxplot: loan_percent_income by status — this is our strongest
    correlated feature (0.38), so it deserves its own dedicated chart.
    """
    fig, ax = plt.subplots(figsize=FIGSIZE_STANDARD)

    sns.boxplot(data=df, x="loan_status", y="loan_percent_income",
                hue="loan_status", palette=PALETTE, legend=False, ax=ax)
    ax.set_title("Loan-to-Income Ratio by Loan Status\n(Strongest Predictor in Dataset)",
                 fontsize=13, fontweight="bold")
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["Rejected", "Approved"])
    ax.set_xlabel("Loan Status")
    ax.set_ylabel("Loan Amount as % of Income")

    _save_and_close(fig, "11_loan_percent_income_impact.png")


def generate_all_charts(df: pd.DataFrame) -> None:
    """Run every chart function in sequence."""
    print("\n--- Generating all charts ---")
    plot_approval_distribution(df)
    plot_income_by_status(df)
    plot_gender_approval(df)
    plot_loan_intent_approval(df)
    plot_credit_score_distribution(df)
    plot_credit_history_length(df)
    plot_loan_amount_distribution(df)
    plot_previous_default_impact(df)
    plot_risk_by_home_ownership(df)
    plot_correlation_heatmap(df)
    plot_loan_percent_income_impact(df)
    print("--- All charts generated successfully ---\n")


if __name__ == "__main__":
    PROCESSED_PATH = os.path.join("data", "processed", "loan_data_cleaned.csv")
    data = pd.read_csv(PROCESSED_PATH)
    generate_all_charts(data)