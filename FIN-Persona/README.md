# FinPersona

AI-powered customer segmentation and personalization pipeline with monitoring.

## Overview

FinPersona is a proof-of-concept data pipeline that generates synthetic banking customer profiles, engineers behavioral features, segments customers into meaningful personas, and generates personalized communication messages using OpenAI. It also exports operational metrics to Prometheus and visualizes them in Grafana.

## Key Features

- Synthetic customer generation for four persona segments
- Feature engineering for risk, spending, savings, and balance behavior
- KMeans clustering-based customer segmentation
- Dynamic marketing strategy assignment per segment
- Personalized message generation via OpenAI prompts
- Prometheus metrics export and Grafana visualization
- Docker Compose deployment for app, Prometheus, and Grafana

## Architecture

The project uses a simple microservice-style architecture with three main containers:

- `finpersona`: Runs the Python pipeline and exposes Prometheus metrics on port `8000`
- `prometheus`: Scrapes application metrics and serves them on port `9090`
- `grafana`: Connects to Prometheus and displays dashboards on port `3000`

The data flow is:

1. Generate synthetic customer records
2. Engineer derived financial features
3. Cluster customers into segments and assign strategies
4. Generate personalized messages using OpenAI
5. Record runtime and business metrics for monitoring

## Prerequisites

- Docker Desktop installed
- Docker Compose available
- OpenAI API key
- (Optional) Windows PowerShell or terminal access

## Setup

1. Clone the repository:

```powershell
git clone https://github.com/not2511/fin-persona "c:\VS code\fin-persona"
cd "c:\VS code\fin-persona"
```

2. Create a `.env` file in the project root with your OpenAI API key:

```text
OPENAI_API_KEY=your_openai_api_key_here
```

3. Verify `docker-compose.yml` and `app/Dockerfile` are present.

## Run the project with Docker Compose

From the project root:

```powershell
docker-compose down
docker-compose up --build
```

This will:

- build the Python application image
- start Prometheus and Grafana
- launch the FinPersona pipeline
- generate 200 synthetic customers
- keep the metrics endpoint alive for scraping

## Accessing the UI

- Grafana: `http://localhost:3000`
- Prometheus: `http://localhost:9090`

Grafana can be configured to visualize the following metrics:

- `finpersona_customers_processed_total`
- `finpersona_messages_total`
- `finpersona_llm_latency_seconds`
- `finpersona_segment_size`
- `finpersona_avg_risk_score`
- `finpersona_avg_balance`
- `finpersona_avg_income`
- `finpersona_pipeline_progress_percent`

## Recommended Grafana panels

1. **Total Customers Processed**
   - Query: `sum(finpersona_customers_processed_total)`
   - Visualization: Stat

2. **Messages Generated Over Time**
   - Query: `sum by (segment, channel) (rate(finpersona_messages_total[1m]))`
   - Visualization: Time series

3. **LLM Latency P95 by Segment**
   - Query: `histogram_quantile(0.95, sum(rate(finpersona_llm_latency_seconds_bucket[5m])) by (le, segment))`
   - Visualization: Time series

4. **Segment Size**
   - Query: `finpersona_segment_size`
   - Visualization: Stat or Table

5. **Pipeline Progress**
   - Query: `finpersona_pipeline_progress_percent`
   - Visualization: Gauge

## Project structure

```
fin-persona/
├── app/
│   ├── data_generator.py        # synthetic customer data generator
│   ├── feature_engineering.py   # derived financial feature creation
│   ├── genai_personalizer.py    # OpenAI prompt builder and requester
│   ├── main.py                 # pipeline orchestration
│   ├── metrics_exporter.py     # Prometheus metric definitions
│   ├── segmentation.py         # clustering and segment labeling
│   ├── requirements.txt        # Python dependencies
│   └── Dockerfile              # container image definition
├── docker-compose.yml          # Compose orchestration for app, Prometheus, Grafana
├── prometheus/
│   └── prometheus.yml          # Prometheus scrape configuration
└── README.md                   # project documentation
```

## Notes

- The pipeline currently generates `200` customers by default.
- The OpenAI integration uses the `OPENAI_API_KEY` from the environment.
- The app keeps running after the pipeline finishes so Prometheus and Grafana can continue scraping metrics.

## Troubleshooting

- If Grafana or Prometheus cannot connect, verify the containers are running in Docker Desktop.
- If OpenAI fails, verify the `.env` file is present and the API key is valid.
- Run `docker-compose down` before `docker-compose up --build` to ensure a clean restart.

## License

This repository is provided for demonstration and learning purposes.

