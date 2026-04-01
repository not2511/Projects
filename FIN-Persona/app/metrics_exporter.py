from prometheus_client import Counter, Histogram, Gauge, start_http_server

def start_metrics_server(port=8000):
    start_http_server(port)
    print(f"📊 Metrics server running on port {port}")


# ── Counters (only go up) ──────────────────────────────────────
messages_generated = Counter(
    "finpersona_messages_total",
    "Total messages generated",
    ["segment", "channel"]
)

customers_processed = Counter(
    "finpersona_customers_processed_total",
    "Total customers processed"
)

# ── Histograms (tracks distribution) ──────────────────────────
llm_latency = Histogram(
    "finpersona_llm_latency_seconds",
    "LLM generation latency in seconds",
    ["segment"],
    buckets=[0.3, 0.5, 0.8, 1.0, 1.5, 2.0, 3.0, 5.0]
)

# ── Gauges (can go up and down) ────────────────────────────────
segment_size = Gauge(
    "finpersona_segment_size",
    "Number of customers per segment",
    ["segment"]
)

avg_risk = Gauge(
    "finpersona_avg_risk_score",
    "Average risk score per segment",
    ["segment"]
)

avg_balance = Gauge(
    "finpersona_avg_balance",
    "Average balance per segment",
    ["segment"]
)

avg_income = Gauge(
    "finpersona_avg_income",
    "Average monthly income per segment",
    ["segment"]
)

pipeline_progress = Gauge(
    "finpersona_pipeline_progress_percent",
    "Percentage of customers processed so far"
)