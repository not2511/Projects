import pandas as pd
import numpy as np

def generate_customers(n=200):
    np.random.seed(42)
    segments_n = n // 4  # 50 each

    def make_segment(n, income_range, balance_range, spend_range,
                     emi_range, missed_range, savings_range):
        return {
            "monthly_income":  np.random.randint(*income_range, n),
            "avg_balance":     np.random.randint(*balance_range, n),
            "monthly_spend":   np.random.randint(*spend_range, n),
            "emi_amount":      np.random.randint(*emi_range, n),
            "missed_payments": np.random.randint(*missed_range, n),
            "savings_account": np.random.randint(*savings_range, n),
        }

    # High-Value Savers: high income, high balance, low spend, low EMI
    hv = make_segment(segments_n,
        income_range=(120000, 200000),
        balance_range=(300000, 500000),
        spend_range=(20000, 50000),
        emi_range=(0, 10000),
        missed_range=(0, 1),
        savings_range=(80000, 100000),
    )

    # At-Risk Defaulters: low income, low balance, high spend, high EMI, missed payments
    ar = make_segment(segments_n,
        income_range=(15000, 35000),
        balance_range=(500, 10000),
        spend_range=(20000, 40000),
        emi_range=(10000, 25000),
        missed_range=(3, 6),
        savings_range=(0, 5000),
    )

    # Active Transactors: medium income, medium balance, very high spend, moderate EMI
    at = make_segment(segments_n,
        income_range=(60000, 100000),
        balance_range=(50000, 150000),
        spend_range=(60000, 120000),
        emi_range=(5000, 20000),
        missed_range=(0, 2),
        savings_range=(10000, 40000),
    )

    # Young Aspirants: low-medium income, low balance, moderate spend, low savings
    ya = make_segment(segments_n,
        income_range=(20000, 45000),
        balance_range=(5000, 40000),
        spend_range=(10000, 30000),
        emi_range=(2000, 10000),
        missed_range=(0, 2),
        savings_range=(1000, 15000),
    )

    # Combine all segments
    total = segments_n * 4
    rows = {}
    for key in hv:
        rows[key] = np.concatenate([hv[key], ar[key], at[key], ya[key]])

    df = pd.DataFrame(rows)
    df.insert(0, "customer_id", [f"C{str(i).zfill(4)}" for i in range(total)])
    df.insert(1, "name", [f"Customer_{i}" for i in range(total)])
    df["age"] = np.concatenate([
        np.random.randint(35, 65, segments_n),  # HV: older
        np.random.randint(25, 45, segments_n),  # AR: working age
        np.random.randint(28, 50, segments_n),  # AT: mid career
        np.random.randint(22, 32, segments_n),  # YA: young
    ])
    df["preferred_channel"] = np.concatenate([
        np.random.choice(["Email", "Push"], segments_n),
        np.random.choice(["SMS", "WhatsApp"], segments_n),
        np.random.choice(["WhatsApp", "Push"], segments_n),
        np.random.choice(["SMS", "WhatsApp"], segments_n),
    ])

    return df


if __name__ == "__main__":
    df = generate_customers()
    print(f" Generated {len(df)} customers")
    print(df.head())
    print(f"\nIncome range: ₹{df['monthly_income'].min():,} – ₹{df['monthly_income'].max():,}")