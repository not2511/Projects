from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

FEATURES = ["spend_ratio", "emi_burden", "savings_ratio",
            "balance_score", "risk_score"]

SEGMENT_STRATEGY = {
    "High-Value Saver":  "Promote wealth management, FD products, and premium banking",
    "At-Risk Defaulter": "Send payment reminders, offer EMI restructuring, financial wellness tips",
    "Active Transactor": "Offer cashback rewards, credit card upgrades, and loyalty points",
    "Young Aspirant":    "Promote SIP investments, first credit card offers, and savings goals"
}

def assign_labels(df):
    """
    Assign segment labels based on actual cluster characteristics,
    not hardcoded cluster numbers.
    """
    profile = df.groupby("cluster")[
        ["risk_score", "savings_ratio", "balance_score", "spend_ratio"]
    ].mean()

    labels = {}

    # Highest savings_ratio + high balance = High-Value Saver
    labels[profile["savings_ratio"].idxmax()] = "High-Value Saver"

    # Highest risk_score = At-Risk Defaulter
    labels[profile["risk_score"].idxmax()] = "At-Risk Defaulter"

    # Highest spend_ratio (excluding already labeled) = Active Transactor
    remaining = [i for i in profile.index if i not in labels]
    labels[
        profile.loc[remaining, "spend_ratio"].idxmax()
    ] = "Active Transactor"

    # Whatever is left = Young Aspirant
    for i in profile.index:
        if i not in labels:
            labels[i] = "Young Aspirant"

    return labels


def segment_customers(df):
    df = df.copy()

    scaler = StandardScaler()
    X = scaler.fit_transform(df[FEATURES])

    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    df["cluster"] = kmeans.fit_predict(X)

    score = silhouette_score(X, df["cluster"])

    # Dynamically assign labels based on cluster behavior
    label_map = assign_labels(df)
    df["segment"] = df["cluster"].map(label_map)
    df["strategy"] = df["segment"].map(SEGMENT_STRATEGY)

    return df, score


if __name__ == "__main__":
    from data_generator import generate_customers
    from feature_engineering import engineer_features

    df = generate_customers()
    df = engineer_features(df)
    df, sil_score = segment_customers(df)

    print(" Segmentation complete")
    print(f"\nSilhouette Score: {sil_score:.3f}")
    print(f"\nSegment Distribution:")
    print(df["segment"].value_counts().to_string())

    print(f"\nSegment Profiles (averages):")
    profile = df.groupby("segment")[
        ["monthly_income", "avg_balance", "risk_score", "savings_ratio"]
    ].mean().round(2)
    print(profile.to_string())