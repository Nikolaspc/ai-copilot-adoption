import csv
import random
import datetime
import os

def generate_mock_metrics(filename="metrics/export.csv"):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    headers = ["request_id", "timestamp", "user_hash", "intent", "latency_ms", "feedback"]
    intents = ["RAG", "Summary", "Action Extraction"]
    
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        for i in range(50):
            writer.writerow([
                f"req-{i}",
                datetime.datetime.now().isoformat(),
                f"user-{random.randint(1, 10)}",
                random.choice(intents),
                random.randint(200, 3500),
                random.choice(["up", "down", "none"])
            ])

if __name__ == "__main__":
    generate_mock_metrics()