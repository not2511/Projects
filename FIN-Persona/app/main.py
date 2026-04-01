import time
import os
from dotenv import load_dotenv

from data_generator import generate_customers
from feature_engineering import engineer_features
from segmentation import segment_customers
from genai_personalizer import generate_message
from metrics_exporter import (
    start_metrics_server,
    messages_generated,
    customers_processed,
    llm_latency,
    segment_size,
    avg_risk,
    avg_balance,
    avg_income,
    pipeline_progress,
)

load_dotenv()


def push_segment_metrics(df):
    """Push segment-level aggregate metrics to Prometheus."""
    for segment in df["segment"].unique():
        seg_df = df[df["segment"] == segment]

        segment_size.labels(segment=segment).set(len(seg_df))
        avg_risk.labels(segment=segment).set(
            round(seg_df["risk_score"].mean(), 3)
        )
        avg_balance.labels(segment=segment).set(
            round(seg_df["avg_balance"].mean(), 2)
        )
        avg_income.labels(segment=segment).set(
            round(seg_df["monthly_income"].mean(), 2)
        )


def run_pipeline():
    print("=" * 60)
    print("FinPersona Pipeline Starting...")
    print("=" * 60)

    # Step 1 — Start metrics server
    start_metrics_server(port=8000)

    # Step 2 — Generate data
    print("\n Generating customer data...")
    df = generate_customers(200)
    print(f"{len(df)} customers generated")

    # Step 3 — Feature engineering
    print("\n  Engineering features...")
    df = engineer_features(df)
    print(" Features ready")

    # Step 4 — Segmentation
    print("\n Segmenting customers...")
    df, sil_score = segment_customers(df)
    print(f"Segmentation complete (silhouette: {sil_score:.3f})")
    print(df["segment"].value_counts().to_string())

    # Step 5 — Push segment-level metrics
    push_segment_metrics(df)
    print("\nSegment metrics pushed to Prometheus")

    # Step 6 — GenAI personalization loop
    print("\n Generating personalized messages...\n")
    print("-" * 60)

    total = len(df)

    for i, (_, customer) in enumerate(df.iterrows()):
        segment  = customer["segment"]
        strategy = customer["strategy"]
        channel  = customer["preferred_channel"]

        try:
            message, latency = generate_message(customer, segment, strategy)

            # Update Prometheus metrics
            messages_generated.labels(
                segment=segment, channel=channel
            ).inc()
            llm_latency.labels(segment=segment).observe(latency)
            customers_processed.inc()
            pipeline_progress.set(round((i + 1) / total * 100, 1))

            print(f"[{i+1:03}/{total}] {segment} | {channel}")
            print(f"         {customer['customer_id']} → {message}")
            print(f"         ⏱ {latency:.2f}s\n")

        except Exception as e:
            print(f"[{i+1:03}/{total}] ❌ Error for {customer['customer_id']}: {e}")

        # Small delay so Grafana shows a live stream not instant spike
        time.sleep(0.3)

    print("=" * 60)
    print("Pipeline complete — all customers processed")
    print(f"Grafana dashboard → http://localhost:3000")
    print(f" Prometheus metrics → http://localhost:9090")
    print("=" * 60)

    # Keep metrics server alive for Grafana to keep scraping
    print("\n Keeping metrics server alive. Press Ctrl+C to stop.\n")
    while True:
        time.sleep(10)


if __name__ == "__main__":
    run_pipeline()