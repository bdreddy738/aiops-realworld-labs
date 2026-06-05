# CODE_EXPLANATION.md

# AIOps Lab Day-01 Code Walkthrough

## Objective

The objective of this document is to explain every source file used in the AIOps project and describe how data flows from Prometheus to Machine Learning and finally to Slack.

---

# Source Files

```text
scripts/
├── config.ini
├── fetch_metrics.py
├── train_model.py
├── detect_anomalies.py
├── requirements.txt
```

---

# End-to-End Code Flow

```text
Prometheus
      │
      ▼
fetch_metrics.py
      │
      ▼
cpu_metrics.csv
      │
      ▼
train_model.py
      │
      ▼
aiops_model.joblib
      │
      ▼
detect_anomalies.py
      │
      ▼
Slack Alert
```

---

# File 1 : config.ini

Location:

```text
scripts/config.ini
```

Purpose:

Store configuration outside source code.

Example:

```ini
[monitoring]

prometheus_url=http://54.196.0.226:9090

query=100 - avg by(instance) (
rate(node_cpu_seconds_total{mode="idle"}[1m])
) * 100

slack_webhook=https://hooks.slack.com/services/XXXX
```

---

## Why use config.ini ?

Without config.ini:

```python
PROM_URL="http://54.196.0.226:9090"
```

Hardcoded values.

Every server change requires code modification.

---

With config.ini:

```python
config.read("config.ini")
```

No code change required.

Only configuration changes.

---

# File 2 : fetch_metrics.py

Purpose:

Collect historical CPU metrics from Prometheus.

---

## Imports

```python
import requests
```

Purpose:

Call Prometheus API.

---

```python
import pandas as pd
```

Purpose:

Create DataFrame.

---

```python
import time
```

Purpose:

Calculate timestamps.

---

```python
import configparser
```

Purpose:

Read config.ini.

---

# Configuration Loading

```python
config = configparser.ConfigParser()
```

Create configuration parser.

---

```python
config.read('config.ini')
```

Read configuration file.

---

```python
PROM_URL = config['monitoring']['prometheus_url']
```

Load Prometheus URL.

---

```python
QUERY = config['monitoring']['query']
```

Load PromQL Query.

---

# Historical Data Collection

Function:

```python
fetch_historical(hours=6)
```

Purpose:

Collect six hours of CPU metrics.

---

## Current Time

```python
end = int(time.time())
```

Example:

```text
1717580000
```

Current UNIX timestamp.

---

## Start Time

```python
start = end - hours * 3600
```

Six hours earlier.

---

# Prometheus API

```python
/api/v1/query_range
```

Purpose:

Retrieve historical data.

---

Request:

```python
requests.get(
f"{PROM_URL}/api/v1/query_range"
)
```

Example:

```text
Get CPU data
for last 6 hours
```

---

# Prometheus Response

Example:

```json
{
 "values":[
  [1717580000,"1.5"],
  [1717580060,"1.7"]
 ]
}
```

---

# Create DataFrame

```python
df = pd.DataFrame(...)
```

Creates:

```text
timestamp    cpu_usage

1717580000   1.5
1717580060   1.7
```

---

# Save CSV

```python
df.to_csv("cpu_metrics.csv")
```

Creates:

```text
cpu_metrics.csv
```

Output:

```text
Saved 24 metrics
```

---

# File 3 : train_model.py

Purpose:

Train Machine Learning model.

---

# Why Machine Learning?

Traditional Monitoring:

```text
CPU > 80%
Alert
```

AIOps:

```text
Learn normal behavior
Detect unusual behavior
```

---

# Isolation Forest

Import:

```python
from sklearn.ensemble import IsolationForest
```

Algorithm:

```text
Unsupervised Anomaly Detection
```

---

# Read Dataset

```python
df = pd.read_csv("cpu_metrics.csv")
```

Input:

```text
timestamp,cpu_usage
```

---

# Data Validation

```python
if len(df) < 10:
```

Require minimum samples.

Reason:

Small datasets create poor models.

---

# Create Model

```python
model = IsolationForest(
contamination=0.05
)
```

Meaning:

```text
5%
```

of data can be abnormal.

---

# Model Training

```python
model.fit(
df["cpu_usage"]
)
```

Learning Process:

```text
1%
2%
1.5%
2.2%
1.9%
```

becomes baseline.

---

# Save Model

```python
joblib.dump(
model,
"aiops_model.joblib"
)
```

Creates:

```text
aiops_model.joblib
```

Think:

```text
Saved Brain
```

---

# File 4 : detect_anomalies.py

Purpose:

Real-time anomaly detection.

---

# Load Model

```python
joblib.load(
"aiops_model.joblib"
)
```

Load trained ML model.

---

# Infinite Monitoring Loop

```python
while True:
```

Purpose:

Run forever.

---

# Current CPU Query

API:

```python
/api/v1/query
```

Difference:

```text
query_range
```

Historical Data.

---

```text
query
```

Current Data.

---

# Get Current CPU

Example:

```text
CPU = 2%
```

---

# Prediction

```python
pred = model.predict([[cpu]])
```

Possible Results:

```text
1
```

Normal

---

```text
-1
```

Anomaly

---

# Normal Flow

Output:

```text
CPU Normal: 2%
```

No Slack Alert.

---

# Anomaly Flow

Output:

```text
CPU Anomaly Detected: 50%
```

---

# Slack Integration

Function:

```python
alert_slack()
```

Uses:

```python
requests.post()
```

Payload:

```json
{
"text":"🚨 CPU Anomaly Detected"
}
```

---

# Slack Result

Channel Receives:

```text
🚨 CPU Anomaly Detected: 50%
```

---

# Why Alert Triggered At 2.9%?

Many people assume:

```text
Alert only above 70%
```

Not true.

Machine Learning compares current behavior against historical behavior.

Training Data:

```text
1.0%
1.1%
1.2%
1.3%
```

Current Value:

```text
2.9%
```

Model says:

```text
Unusual Pattern
```

Therefore:

```text
Anomaly
```

---

# Stress Testing

Command:

```bash
stress-ng --cpu 2 --timeout 120s
```

Purpose:

Generate CPU load.

---

Before:

```text
CPU = 2%
```

After:

```text
CPU = 50%
CPU = 100%
```

---

Model Response:

```text
CPU Anomaly Detected
```

---

Slack Response:

```text
Slack alert sent
```

---

# Summary

This project implements an AIOps workflow where historical CPU metrics are collected from Prometheus, used to train an Isolation Forest machine learning model, and continuously evaluated in real time. When abnormal CPU behavior is detected, Slack notifications are automatically generated while Grafana provides operational dashboards for visualization.

# End of Document
