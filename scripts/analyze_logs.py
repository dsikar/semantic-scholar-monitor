import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

LOG_FILE = "request_logs.csv"
PLOTS_DIR = "plots"

def analyze_logs():
    """Analyze request logs for patterns and save plots as images with unique timestamps."""
    try:
        # Ensure the plots directory exists
        if not os.path.exists(PLOTS_DIR):
            os.makedirs(PLOTS_DIR)
        
        # Generate a timestamp for file naming
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Load the log file
        df = pd.read_csv(LOG_FILE)
        
        # Convert Timestamp to datetime
        df["Timestamp"] = pd.to_datetime(df["Timestamp"])
        
        # Compare success rates by mode
        success_rates = df.groupby(["Mode", "Result"]).size().unstack(fill_value=0)
        success_rates["SuccessRate"] = (success_rates["Success"] / success_rates.sum(axis=1)) * 100

        # Plot success rate by mode
        plt.figure(figsize=(10, 5))
        success_rates["SuccessRate"].plot(kind="bar", title="Success Rate by Mode")
        plt.ylabel("Success Rate (%)")
        filename = os.path.join(PLOTS_DIR, f"success_rate_by_mode_{timestamp}.png")
        plt.savefig(filename)
        plt.close()

        # Additional analysis by hour
        for mode in ["Python", "cURL"]:
            mode_data = df[df["Mode"] == mode]
            hourly_success = mode_data[mode_data["Result"] == "Success"].groupby("Hour").size()
            hourly_total = mode_data.groupby("Hour").size()
            hourly_rate = (hourly_success / hourly_total) * 100

            plt.figure(figsize=(10, 5))
            hourly_rate.plot(kind="bar", title=f"Hourly Success Rate - {mode}")
            plt.xlabel("Hour of Day")
            plt.ylabel("Success Rate (%)")
            filename = os.path.join(PLOTS_DIR, f"hourly_success_rate_{mode.lower()}_{timestamp}.png")
            plt.savefig(filename)
            plt.close()

        # Additional analysis by day of the week
        daily_success = df[df["Result"] == "Success"].groupby("DayOfWeek").size()
        daily_total = df.groupby("DayOfWeek").size()
        daily_rate = (daily_success / daily_total) * 100

        plt.figure(figsize=(10, 5))
        daily_rate.reindex(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]).plot(
            kind="bar", title="Success Rate by Day of Week"
        )
        plt.xlabel("Day of Week")
        plt.ylabel("Success Rate (%)")
        filename = os.path.join(PLOTS_DIR, f"success_rate_by_day_of_week_{timestamp}.png")
        plt.savefig(filename)
        plt.close()

        print(f"Plots have been saved to the '{PLOTS_DIR}' directory with timestamp {timestamp}.")
    
    except Exception as e:
        print(f"Error analyzing logs: {e}")

if __name__ == "__main__":
    analyze_logs()
