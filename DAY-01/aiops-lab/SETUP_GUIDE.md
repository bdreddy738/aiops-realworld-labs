# AIOps Lab Day-01: CPU Anomaly Detection Using Prometheus, Grafana, Python ML & Slack

## Project Overview

This project demonstrates an AIOps use case where infrastructure CPU metrics are collected from Prometheus, analyzed using a Machine Learning model (Isolation Forest), and anomalies are automatically detected and sent to Slack.

### Architecture

```text
Node Exporter
      ↓
Prometheus
      ↓
Python ML Model (Isolation Forest)
      ↓
Anomaly Detection
      ↓
Slack Notification
      ↓
Grafana Dashboard
```

---

# Prerequisites

## AWS

* AWS Account
* EC2 Instance (Amazon Linux 2023)
* Security Group Access

## Local System

* Browser
* GitHub Account
* Slack Workspace
* MobaXterm (optional)

---

# Step 1: Launch EC2 Instance

## Instance Configuration

| Setting        | Value             |
| -------------- | ----------------- |
| AMI            | Amazon Linux 2023 |
| Instance Type  | t3.micro          |
| Storage        | 8 GB              |
| Security Group | Custom            |

---

## Security Group Rules

Add inbound rules:

| Port | Purpose       |
| ---- | ------------- |
| 22   | SSH           |
| 3000 | Grafana       |
| 9090 | Prometheus    |
| 9100 | Node Exporter |

Source:

```text
0.0.0.0/0
```

For production:

```text
Use your office/public IP only
```

---

# Step 2: Connect to EC2

Using EC2 Instance Connect:

```bash
sudo su -
```

Verify:

```bash
whoami
```

Expected:

```text
root
```

---

# Step 3: Install Git

Amazon Linux:

```bash
dnf install git -y
```

Verify:

```bash
git --version
```

---

# Step 4: Clone Repository

```bash
git clone https://github.com/bdreddy738/aiops-realworld-labs.git
```

Move into project:

```bash
cd aiops-realworld-labs/DAY-01/aiops-lab
```

Verify:

```bash
ls
```

Expected:

```text
config
scripts
docker-compose.yml
README.md
```

---

# Step 5: Install Docker

```bash
dnf install docker -y
```

Start Docker:

```bash
systemctl enable docker
systemctl start docker
```

Verify:

```bash
docker --version
```

---

# Step 6: Install Docker Compose

Amazon Linux 2023 already supports:

```bash
docker compose
```

Verify:

```bash
docker compose version
```

---

# Step 7: Create Python Virtual Environment

Install Python Tools:

```bash
dnf install python3 python3-pip -y
```

Create venv:

```bash
python3 -m venv venv
```

Activate:

```bash
source venv/bin/activate
```

Expected:

```text
(venv)
```

---

# Why Virtual Environment?

Without venv:

```text
Packages install globally
Version conflicts possible
```

With venv:

```text
Project isolated
Safe package management
Portable environment
```

---

# Step 8: Install Python Packages

```bash
pip install -r scripts/requirements.txt
```

If package conflicts occur:

```bash
pip install pandas requests scikit-learn joblib configparser
```

Verify:

```bash
python3 -c "import requests,pandas,sklearn,joblib; print('OK')"
```

Expected:

```text
OK
```

---

# Step 9: Configure Slack Webhook

Create Slack Incoming Webhook.

Navigate:

```text
Slack Apps
→ Incoming Webhooks
→ Activate Incoming Webhooks
→ Add New Webhook
```

Copy Webhook URL.

---

Edit:

```bash
cd scripts
vi config.ini
```

Update:

```ini
[monitoring]
prometheus_url = http://<EC2_PUBLIC_IP>:9090

query = 100 - avg by(instance) (
rate(node_cpu_seconds_total{mode="idle"}[1m])
) * 100

slack_webhook = https://hooks.slack.com/services/XXXX
```

Verify:

```bash
cat config.ini
```

---

# Step 10: Start Monitoring Stack

Return project root:

```bash
cd ..
```

Run:

```bash
docker compose up -d
```

Verify:

```bash
docker ps
```

Expected:

```text
Prometheus
Grafana
Node Exporter
```

All containers should be UP.

---

# Step 11: Access Dashboards

## Prometheus

```text
http://<PUBLIC-IP>:9090
```

Example:

```text
http://54.196.0.226:9090
```

---

## Grafana

```text
http://<PUBLIC-IP>:3000
```

Login:

```text
admin
admin
```

---

# Step 12: Configure Grafana

Add Data Source.

Navigate:

```text
Connections
→ Data Sources
→ Add Data Source
→ Prometheus
```

URL:

```text
http://prometheus:9090
```

Save & Test.

Expected:

```text
Data source is working
```

---

# Step 13: Import Dashboard

Navigate:

```text
Dashboards
→ Import
```

Dashboard ID:

```text
1860
```

Import.

Select:

```text
Prometheus datasource
```

Result:

```text
Node Exporter Full Dashboard
```

---

# Step 14: Collect Historical Metrics

Move into scripts:

```bash
cd scripts
```

Activate venv:

```bash
source ../venv/bin/activate
```

Run:

```bash
python3 fetch_metrics.py
```

Expected:

```text
Saved XX metrics to cpu_metrics.csv
```

Generated:

```text
cpu_metrics.csv
```

---

# Step 15: Train Machine Learning Model

Run:

```bash
python3 train_model.py
```

Expected:

```text
Model trained and saved
```

Generated:

```text
aiops_model.joblib
```

---

# Step 16: Start Real-Time Detection

Run:

```bash
python3 detect_anomalies.py
```

Expected:

```text
AIOps detector started
CPU Normal: X%
```

This process remains running continuously.

---

# Step 17: Open Second Terminal

Use:

```text
MobaXterm
```

Connect to same EC2 instance.

This allows:

Terminal 1:

```text
detect_anomalies.py
```

Terminal 2:

```text
stress testing
```

---

# Step 18: Install Stress Tool

Amazon Linux:

```bash
dnf install stress-ng -y
```

Verify:

```bash
stress-ng --version
```

---

# Step 19: Generate CPU Load

Run:

```bash
stress-ng --cpu 2 --timeout 120s
```

Meaning:

```text
Use 2 CPU workers
Run for 120 seconds
```

---

# Step 20: Observe Anomaly Detection

Terminal 1:

Expected:

```text
CPU Anomaly Detected: 50%
Slack alert sent

CPU Anomaly Detected: 100%
Slack alert sent
```

---

# Step 21: Verify Slack Alerts

Open Slack channel.

Expected:

```text
🚨 CPU Anomaly Detected: 50%

🚨 CPU Anomaly Detected: 100%
```

---

# Step 22: Verify Grafana Dashboard

Open:

```text
http://<PUBLIC-IP>:3000
```

Observe:

```text
CPU Usage Spike
Memory Usage
System Load
Network Metrics
```

---

# Files Created During Execution

```text
cpu_metrics.csv
```

Historical metrics dataset.

---

```text
aiops_model.joblib
```

Trained ML model.

---

# Project Components

| Component        | Purpose              |
| ---------------- | -------------------- |
| Docker           | Container Runtime    |
| Prometheus       | Metrics Collection   |
| Node Exporter    | Linux Metrics        |
| Grafana          | Visualization        |
| Python           | Automation           |
| Isolation Forest | ML Anomaly Detection |
| Slack            | Alerting             |
| stress-ng        | Load Simulation      |

---

# Note :

This project implements an AIOps workflow using Prometheus, Grafana, Python, Docker, Slack, and Machine Learning. Infrastructure metrics are collected through Node Exporter and stored in Prometheus. Historical CPU data is extracted and used to train an Isolation Forest anomaly detection model. During runtime, real-time CPU metrics are continuously evaluated against the trained model. When abnormal behavior is detected, alerts are automatically pushed to Slack while Grafana provides visual monitoring dashboards for operational visibility.

# End of Document
