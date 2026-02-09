import pandas as pd

def generate_summary():
    try:
        df = pd.read_csv("metrics/usage_logs.csv")
        summary = {
            "Total Queries": len(df),
            "Avg Latency (ms)": df["latency_ms"].mean(),
            "Positive Feedback %": (len(df[df["feedback_score"] == "up"]) / len(df)) * 100
        }
        print("--- AI Co-Pilot KPI Summary ---")
        for k, v in summary.items():
            print(f"{k}: {v:.2f}")
    except Exception:
        print("No metrics data found yet.")

if __name__ == "__main__":
    generate_summary()