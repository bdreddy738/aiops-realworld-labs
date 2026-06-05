# Copyright (c) 2026 cloudhiredofficial
# All rights reserved.

# Used to call Prometheus REST APIs
import requests

# Used to create DataFrames and save CSV files
import pandas as pd

# Used for timestamp calculations
import time

# Used to check whether files exist
import os

# Used to read config.ini file
import configparser

# Create configuration parser object
config = configparser.ConfigParser()

# Read configuration from config.ini
config.read('config.ini')

# Load Prometheus URL from config.ini
PROM_URL = config['monitoring']['prometheus_url']

# Load PromQL query from config.ini
QUERY = config['monitoring']['query']


# Function to fetch historical CPU metrics from Prometheus
# Default = last 1 hour
def fetch_historical(hours=1):
    try:

        # Verify config.ini exists before continuing
        if not os.path.exists('config.ini'):
            raise FileNotFoundError("config.ini not found")

        # Current UNIX timestamp
        # Example: 1750000000
        end = int(time.time())

        # Calculate start time
        # Example:
        # hours=6
        # start = current time - 6 hours
        start = end - hours * 3600

        # Call Prometheus Historical Query API
        response = requests.get(

            # Prometheus endpoint for historical data
            # Example:
            # http://prometheus:9090/api/v1/query_range
            f"{PROM_URL}/api/v1/query_range",

            # Query parameters
            params={

                # CPU usage PromQL query
                "query": QUERY,

                # Historical start timestamp
                "start": start,

                # Historical end timestamp
                "end": end,

                # Collect one sample every 60 seconds
                "step": "60s"
            },

            # Maximum wait time
            timeout=10
        )

        # Raise exception if API returns 404/500/etc
        response.raise_for_status()

        # Convert JSON response into Python dictionary
        data = response.json()

        # Verify metrics were returned
        # If empty, Node Exporter or Prometheus may have issues
        if not data["data"]["result"]:
            raise ValueError(
                "No data received - check node_exporter connection"
            )

        # Extract historical metric values
        # Example:
        # [
        #   [1717000000, "1.2"],
        #   [1717000060, "1.5"]
        # ]
        points = data["data"]["result"][0]["values"]

        # Create DataFrame
        # Columns:
        # timestamp
        # cpu_usage
        df = pd.DataFrame(
            points,
            columns=["timestamp", "cpu_usage"]
        )

        # Convert CPU values from string to float
        # Example:
        # "1.5" -> 1.5
        df["cpu_usage"] = df["cpu_usage"].astype(float)

        # Save metrics into CSV file
        # Output:
        # cpu_metrics.csv
        df.to_csv(
            "cpu_metrics.csv",
            index=False
        )

        # Success message
        print(
            f"✅ Saved {len(df)} metrics to cpu_metrics.csv"
        )

    # Handle network-related errors
    except requests.exceptions.RequestException as e:

        print(f"❌ Network Error: {str(e)}")

    # Handle all other errors
    except Exception as e:

        print(f"❌ Error: {str(e)}")


# Program starting point
if __name__ == "__main__":

    # Collect last 6 hours of CPU data
    # Used as training dataset for ML model
    fetch_historical(hours=6)