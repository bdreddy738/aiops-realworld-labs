git clone

docker compose up -d

source venv/bin/activate

python3 fetch_metrics.py

python3 train_model.py

python3 detect_anomalies.py

stress-ng --cpu 2 --timeout 120s