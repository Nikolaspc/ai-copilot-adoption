import csv
import os
from datetime import datetime

METRICS_FILE = "metrics/usage_logs.csv"

class Telemetry:
    def __init__(self):
        os.makedirs("metrics", exist_ok=True)
        if not os.path.exists(METRICS_FILE):
            self._create_header()

    def _create_header(self):
        headers = ["timestamp", "user_id", "query_length", "latency_ms", "feedback_score"]
        with open(METRICS_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)

    def log_interaction(self, user_id, query, latency, feedback=None):
        with open(METRICS_FILE, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.now().isoformat(),
                user_id,
                len(query),
                latency,
                feedback if feedback else "N/A"
            ])