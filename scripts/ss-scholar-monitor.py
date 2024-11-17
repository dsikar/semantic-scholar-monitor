import requests
import subprocess
import schedule
import time
import pandas as pd
import random
from datetime import datetime
from scripts.analyze_logs import analyze_logs  # Import the analysis function

# Constants
PAPER_IDS_FILE = "paper_ids.txt"
LOG_FILE = "request_logs.csv"

def load_paper_ids():
    """Load paper IDs from a file."""
    try:
        with open(PAPER_IDS_FILE, "r") as file:
            paper_ids = [line.strip() for line in file if line.strip()]
        return paper_ids
    except Exception as e:
        print(f"Error loading paper IDs: {e}")
        return []

def make_python_request(paper_ids):
    """Make a GET request using Python's requests library."""
    paper_id = random.choice(paper_ids)
    url = f"https://api.semanticscholar.org/graph/v1/paper/{paper_id}/authors"
    params = {"fields": "url,papers.title,papers.year,papers.authors,papers.abstract", "offset": 2}
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    day_of_week = datetime.now().strftime("%A")
    try:
        response = requests.get(url, params=params)
        status_code = response.status_code
        result = "Success" if status_code == 200 else "Failure"
        print(f"[Python - {timestamp}] {result} - Status Code: {status_code} - Paper ID: {paper_id}")
    except Exception as e:
        result = "Error"
        status_code = None
        print(f"[Python - {timestamp}] Error - {e} - Paper ID: {paper_id}")
    
    log_entry = {
        "Timestamp": timestamp,
        "DayOfWeek": day_of_week,
        "Hour": datetime.now().hour,
        "Mode": "Python",
        "Result": result,
        "StatusCode": status_code,
        "PaperID": paper_id,
    }
    log_to_file(log_entry)

def make_curl_request(paper_ids):
    """Make a GET request using the curl command."""
    paper_id = random.choice(paper_ids)
    url = f"https://api.semanticscholar.org/graph/v1/paper/{paper_id}/authors"
    params = "fields=url,papers.title,papers.year,papers.authors,papers.abstract&offset=2"
    full_url = f"{url}?{params}"

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    day_of_week = datetime.now().strftime("%A")
    try:
        curl_command = [
            "curl",
            "-s",
            "-o", "/dev/null",
            "-w", "%{http_code}",
            full_url
        ]
        result = subprocess.run(curl_command, capture_output=True, text=True)
        status_code = int(result.stdout.strip())
        result_status = "Success" if status_code == 200 else "Failure"
        print(f"[cURL - {timestamp}] {result_status} - Status Code: {status_code} - Paper ID: {paper_id}")
    except Exception as e:
        result_status = "Error"
        status_code = None
        print(f"[cURL - {timestamp}] Error - {e} - Paper ID: {paper_id}")
    
    log_entry = {
        "Timestamp": timestamp,
        "DayOfWeek": day_of_week,
        "Hour": datetime.now().hour,
        "Mode": "cURL",
        "Result": result_status,
        "StatusCode": status_code,
        "PaperID": paper_id,
    }
    log_to_file(log_entry)

def log_to_file(entry):
    """Append log entry to CSV file."""
    try:
        df = pd.DataFrame([entry])
        df.to_csv(LOG_FILE, mode="a", header=not pd.io.common.file_exists(LOG_FILE), index=False)
    except Exception as e:
        print(f"Failed to log entry: {e}")

# Load paper IDs once at the start
paper_ids = load_paper_ids()

if not paper_ids:
    print("No paper IDs available. Exiting...")
    exit(1)

# Schedule tasks
schedule.every(30).minutes.do(make_python_request, paper_ids=paper_ids)
schedule.every(30).minutes.do(make_curl_request, paper_ids=paper_ids)

# Schedule daily log analysis
schedule.every().day.at("00:00").do(analyze_logs)

if __name__ == "__main__":
    print("Starting request monitoring and daily analysis...")
    while True:
        schedule.run_pending()
        time.sleep(1)
