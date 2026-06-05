# PROMETHEUS_GUIDE.md

# Complete Prometheus Guide for AIOps Lab

## Objective

This document explains Prometheus architecture, installation, configuration, metric collection, PromQL queries, and how Prometheus integrates with the AIOps anomaly detection solution.

---

# What is Prometheus?

Prometheus is an open-source monitoring and alerting system originally developed by SoundCloud and now maintained by the CNCF.

Purpose:

```text
Collect Metrics
Store Metrics
Query Metrics
Monitor Infrastructure
```

---

# Why Prometheus?

Traditional monitoring:

```text
Server Down
Application Down
Disk Full
```

Modern monitoring:

```text
CPU
Memory
Disk
Containers
Kubernetes
Applications
Network
```

Prometheus solves this problem.

---

# Prometheus Architecture

```text
Node Exporter
      │
      ▼
Prometheus
      │
      ▼
Grafana
      │
      ▼
Users
```

In our AIOps project:

```text
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
```

---

# Key Components

## Prometheus Server

Purpose:

```text
Collect Metrics
Store Metrics
Execute Queries
```

Port:

```text
9090
```

---

## Exporters

Prometheus does not collect metrics directly.

Exporters expose metrics.

Examples:

```text
Node Exporter
MySQL Exporter
Redis Exporter
Blackbox Exporter
Kubernetes Exporter
```

Our project uses:

```text
Node Exporter
```

---

## Time Series Database

Prometheus stores:

```text
Metric Name
Timestamp
Value
```

Example:

```text
cpu_usage

10:00 -> 1.5
10:01 -> 1.8
10:02 -> 2.1
10:03 -> 50.0
```

This becomes historical data.

---

# Installation

Container:

```yaml
prometheus:
  image: prom/prometheus:latest
```

Purpose:

```text
Run Prometheus Server
```

---

# Docker Mapping

```yaml
ports:
  - "9090:9090"
```

Meaning:

```text
Host Port      Container Port

9090     ->       9090
```

Access:

```text
http://SERVER-IP:9090
```

Example:

```text
http://54.196.0.226:9090
```

---

# Prometheus Configuration

File:

```text
config/prometheus.yml
```

---

# Global Section

```yaml
global:
  scrape_interval: 15s
```

Meaning:

Every 15 seconds Prometheus collects metrics.

---

Example

```text
10:00:00
10:00:15
10:00:30
10:00:45
```

Metrics collected every 15 seconds.

---

# Scrape Configurations

```yaml
scrape_configs:
```

Purpose:

Tell Prometheus:

```text
What should I monitor?
```

---

# Job Name

```yaml
job_name: 'node'
```

Logical monitoring name.

Used internally.

---

# Targets

```yaml
targets:
  - 'node_exporter:9100'
```

Meaning:

Collect metrics from:

```text
Container Name
node_exporter

Port
9100
```

---

# Why node_exporter?

Docker network resolves:

```text
node_exporter
```

to container IP.

No manual IP required.

---

# Verify Prometheus

Access:

```text
http://SERVER-IP:9090
```

Expected:

```text
Prometheus Dashboard
```

---

# Health Check

Check:

```bash
curl http://localhost:9090/-/healthy
```

Expected:

```text
Prometheus is Healthy
```

---

# Readiness Check

```bash
curl http://localhost:9090/-/ready
```

Expected:

```text
Prometheus is Ready
```

---

# Metrics Collection Flow

Step 1

Node Exporter exposes metrics.

```text
CPU
Memory
Disk
Network
```

---

Step 2

Prometheus scrapes metrics.

```text
Every 15 seconds
```

---

Step 3

Prometheus stores metrics.

```text
Time Series Database
```

---

Step 4

Grafana reads metrics.

---

Step 5

Python ML reads metrics.

---

# Prometheus API

Prometheus provides REST APIs.

---

# Current Data API

```text
/api/v1/query
```

Purpose:

Current value.

Example:

```text
Current CPU Usage
```

Used by:

```python
detect_anomalies.py
```

---

Example Request

```bash
curl http://localhost:9090/api/v1/query
```

---

# Historical Data API

```text
/api/v1/query_range
```

Purpose:

Historical data.

Example:

```text
Last 6 Hours CPU Usage
```

Used by:

```python
fetch_metrics.py
```

---

# Difference

Current Value:

```text
/api/v1/query
```

Historical Value:

```text
/api/v1/query_range
```

---

# PromQL

Prometheus Query Language.

Similar to:

```text
SQL for Databases
```

PromQL for Prometheus.

---

# CPU Query Used in Project

```promql
100 - avg by(instance)(
rate(node_cpu_seconds_total{mode="idle"}[1m])
) * 100
```

Purpose:

```text
CPU Utilization %
```

---

# Understanding Query

Metric:

```promql
node_cpu_seconds_total
```

CPU metric.

---

Filter:

```promql
mode="idle"
```

Idle CPU.

---

Rate:

```promql
rate(...[1m])
```

Average over 1 minute.

---

Average:

```promql
avg by(instance)
```

Average per server.

---

Convert to CPU Usage

```promql
100 - idle
```

Example:

```text
Idle = 98%

CPU = 100 - 98

CPU = 2%
```

---

# Useful PromQL Queries

## CPU Usage

```promql
100 - avg by(instance)(
rate(node_cpu_seconds_total{mode="idle"}[1m])
) * 100
```

---

## Memory Usage

```promql
(
node_memory_MemTotal_bytes -
node_memory_MemAvailable_bytes
)
/
node_memory_MemTotal_bytes * 100
```

---

## Disk Usage

```promql
100 -
(
node_filesystem_avail_bytes
/
node_filesystem_size_bytes
) * 100
```

---

## Load Average

```promql
node_load1
```

---

# Prometheus in AIOps Flow

Without Prometheus:

```text
No Metrics
No Data
No ML Training
No Detection
```

---

With Prometheus:

```text
Metrics Available
Historical Data Available
Real-Time Data Available
ML Can Train
Anomalies Can Be Detected
```

---

# Interview Questions

## What is Prometheus?

Prometheus is an open-source monitoring and alerting system used to collect, store, query, and monitor time-series metrics.

---

## What is a scrape?

A scrape is the process of collecting metrics from a target endpoint at a configured interval.

---

## What is PromQL?

PromQL is Prometheus Query Language used to query and analyze metrics stored in Prometheus.

---

## Difference Between Query and Query Range?

```text
query
```

Current value.

```text
query_range
```

Historical values.

---

## Why Prometheus in this project?

Prometheus provides historical and real-time CPU metrics that are used for machine learning model training and anomaly detection.

---

# Summary

Prometheus acts as the central metrics platform in this AIOps solution. It continuously collects CPU metrics from Node Exporter, stores them as time-series data, provides APIs for historical and real-time access, and supplies the data required for anomaly detection, Slack alerting, and Grafana visualization.

# End of Document
