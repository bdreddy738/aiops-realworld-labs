# GRAFANA_GUIDE.md

# Complete Grafana Guide for AIOps Lab

## Objective

This document explains Grafana architecture, dashboards, data sources, visualizations, panels, dashboard imports, and how Grafana integrates with Prometheus and the AIOps solution.

---

# What is Grafana?

Grafana is an open-source visualization platform.

Purpose:

```text id="1"
Collect Metrics      ❌
Store Metrics        ❌
Visualize Metrics    ✅
Dashboards           ✅
Charts               ✅
Alerting             ✅
```

---

# Why Grafana?

Prometheus stores data.

Example:

```text id="2"
CPU = 1%
CPU = 2%
CPU = 3%
CPU = 50%
```

Prometheus stores it.

Grafana visualizes it.

Example:

```text id="3"
CPU Usage Chart
Memory Chart
Disk Chart
Network Chart
```

---

# Architecture

```text id="4"
Node Exporter
      │
      ▼
Prometheus
      │
      ▼
Grafana
      │
      ▼
Dashboard
```

In our project:

```text id="5"
Node Exporter
      │
      ▼
Prometheus
      │
      ▼
Python ML
      │
      ▼
Slack

      AND

Prometheus
      │
      ▼
Grafana
```

---

# Grafana Container

Docker Compose:

```yaml id="6"
grafana:
  image: grafana/grafana-enterprise:latest
```

Purpose:

```text id="7"
Visualization Layer
```

---

# Port Mapping

```yaml id="8"
ports:
  - "3000:3000"
```

Meaning:

```text id="9"
Host Port      Container Port

3000    --->      3000
```

Access:

```text id="10"
http://SERVER-IP:3000
```

Example:

```text id="11"
http://54.196.0.226:3000
```

---

# First Login

Default Credentials:

```text id="12"
Username: admin
Password: admin
```

After first login:

Grafana requests password change.

---

# Grafana Components

## Data Source

Data Source means:

```text id="13"
Where is data coming from?
```

Examples:

```text id="14"
Prometheus
MySQL
PostgreSQL
InfluxDB
CloudWatch
Azure Monitor
```

In our project:

```text id="15"
Prometheus
```

---

## Dashboard

Dashboard is:

```text id="16"
Collection of Panels
```

Example:

```text id="17"
CPU Panel
Memory Panel
Disk Panel
Network Panel
```

Combined:

```text id="18"
Dashboard
```

---

## Panel

Panel is:

```text id="19"
Single Chart
```

Example:

```text id="20"
CPU Usage Graph
```

---

# Add Prometheus Data Source

Navigate:

```text id="21"
Connections
→ Data Sources
→ Add Data Source
```

Select:

```text id="22"
Prometheus
```

---

# Prometheus URL

In Docker:

```text id="23"
http://prometheus:9090
```

Reason:

Docker network resolves:

```text id="24"
prometheus
```

to Prometheus container.

---

Alternative:

```text id="25"
http://54.196.0.226:9090
```

---

# Save & Test

Click:

```text id="26"
Save & Test
```

Expected:

```text id="27"
Data source is working
```

---

# Dashboard Import

Grafana provides thousands of dashboards.

Instead of building manually:

Import pre-built dashboards.

---

# Dashboard ID 1860

Most popular Node Exporter dashboard.

ID:

```text id="28"
1860
```

---

# Import Dashboard

Navigate:

```text id="29"
Dashboards
→ Import
```

Enter:

```text id="30"
1860
```

Click:

```text id="31"
Load
```

Select:

```text id="32"
Prometheus Data Source
```

Click:

```text id="33"
Import
```

---

# What Dashboard 1860 Shows

CPU

```text id="34"
CPU Utilization
CPU Load
CPU Core Usage
```

---

Memory

```text id="35"
Used Memory
Available Memory
Swap Usage
```

---

Disk

```text id="36"
Disk Utilization
Filesystem Usage
```

---

Network

```text id="37"
RX Traffic
TX Traffic
Errors
```

---

System

```text id="38"
Uptime
Load Average
Processes
```

---

# Create Custom Dashboard

Navigate:

```text id="39"
Dashboards
→ New Dashboard
```

---

Add Visualization

```text id="40"
Add Panel
```

---

# CPU Panel

Query:

```promql id="41"
100 - avg by(instance)(
rate(node_cpu_seconds_total{mode="idle"}[1m])
) * 100
```

Title:

```text id="42"
CPU Utilization %
```

---

# Memory Panel

Query:

```promql id="43"
(
node_memory_MemTotal_bytes -
node_memory_MemAvailable_bytes
)
/
node_memory_MemTotal_bytes * 100
```

Title:

```text id="44"
Memory Usage %
```

---

# Disk Panel

Query:

```promql id="45"
100 -
(
node_filesystem_avail_bytes
/
node_filesystem_size_bytes
) * 100
```

Title:

```text id="46"
Disk Usage %
```

---

# Why Grafana is Important in AIOps?

Without Grafana:

```text id="47"
Raw Metrics
Raw Numbers
```

Example:

```text id="48"
CPU = 2
CPU = 4
CPU = 50
CPU = 100
```

Hard to understand.

---

With Grafana:

```text id="49"
Visual Charts
Trend Analysis
Capacity Planning
Historical Analysis
```

Easy to understand.

---

# During Stress Test

You executed:

```bash id="50"
stress-ng --cpu 2 --timeout 120s
```

---

CPU changed:

```text id="51"
2%
10%
30%
50%
100%
```

---

Grafana shows:

```text id="52"
Large CPU Spike
```

---

At same time:

```text id="53"
ML Model
```

detects anomaly.

---

Slack receives:

```text id="54"
CPU Anomaly Detected
```

---

# Grafana vs Prometheus

| Feature           | Prometheus | Grafana   |
| ----------------- | ---------- | --------- |
| Collect Metrics   | Yes        | No        |
| Store Metrics     | Yes        | No        |
| Query Metrics     | Yes        | Yes       |
| Visualize Metrics | Limited    | Excellent |
| Dashboards        | Basic      | Advanced  |
| Charts            | Basic      | Advanced  |

---

# Grafana in This Project

```text id="55"
Prometheus
      │
      ▼
Stores CPU Data
      │
      ▼
Grafana Reads Data
      │
      ▼
Displays CPU Graph
```

---

# Troubleshooting

## Dashboard Empty

Check:

```text id="56"
Prometheus datasource connected?
```

---

## No Metrics

Check:

```bash id="57"
docker ps
```

Verify:

```text id="58"
prometheus
node_exporter
grafana
```

Running.

---

## Data Source Error

Verify:

```text id="59"
http://prometheus:9090
```

reachable from Grafana.

---

# Interview Questions

## What is Grafana?

Grafana is an open-source visualization platform used to build dashboards and monitor infrastructure, applications, and business metrics.

---

## Does Grafana Store Data?

No.

Grafana visualizes data.

Prometheus stores data.

---

## What is a Data Source?

A system that provides data to Grafana.

Examples:

```text id="60"
Prometheus
CloudWatch
MySQL
Azure Monitor
```

---

## What is a Dashboard?

A collection of panels displaying metrics and visualizations.

---

## Why Grafana in This Project?

Grafana provides visual monitoring of CPU, memory, disk, and infrastructure metrics while the ML engine performs anomaly detection and Slack handles notifications.

---

# Summary

Grafana serves as the visualization layer of the AIOps platform. It connects to Prometheus, retrieves infrastructure metrics, and displays them through dashboards and charts. During anomaly testing, Grafana visually confirms the CPU spike while the machine learning model detects the anomaly and Slack generates alerts.

# End of Document
