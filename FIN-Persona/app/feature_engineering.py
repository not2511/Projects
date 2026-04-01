import pandas as pd

def engineer_features(df):
    df = df.copy()

    # how much of income is being spent (higher = more financial pressure)
    df["spend_ratio"] = df["monthly_spend"] / df["monthly_income"]

    # EMI as a fraction of income (higher = more debt burden)
    df["emi_burden"] = df["emi_amount"] / df["monthly_income"]

    # Savings relative to income (higher = more financially stable)
    df["savings_ratio"] = df["savings_account"] / df["monthly_income"]

    # Balance health (how many months of income sitting in account)
    df["balance_score"] = df["avg_balance"] / df["monthly_income"]

    # Composite risk score (higher = more at risk)
    df["risk_score"] = (
        df["missed_payments"] * 0.4 +
        df["spend_ratio"]     * 0.3 +
        df["emi_burden"]      * 0.3
    ).round(4)

    return df


if __name__ == "__main__":
    from data_generator import generate_customers

    df = generate_customers()
    df = engineer_features(df)

    print(" Features engineered successfully")
    print(f"\nNew columns added:")
    new_cols = ["spend_ratio", "emi_burden", "savings_ratio",
                "balance_score", "risk_score"]
    print(df[new_cols].describe().round(3))

    print(f"\nHighest risk customer:")
    top_risk = df.loc[df["risk_score"].idxmax()]
    print(f"  ID: {top_risk['customer_id']}")
    print(f"  Risk Score: {top_risk['risk_score']}")
    print(f"  Missed Payments: {top_risk['missed_payments']}")
    print(f"  Spend Ratio: {top_risk['spend_ratio']:.2f}")