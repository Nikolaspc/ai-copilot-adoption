import sys
import os

# Adjust path to ensure the 'app' package is discoverable from the root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from app.core.telemetry import generate_mock_data
except ImportError:
    from core.telemetry import generate_mock_data

if __name__ == "__main__":
    """
    Utility script to prepare the environment for a stakeholder demo.
    Run this to populate the 'Download KPIs' section in the UI.
    """
    print("🚀 AI Co-Pilot: Starting KPI Simulation...")
    generate_mock_data()
    print("Done. You can now download the CSV from the Web UI or check 'data/metrics.csv'.")