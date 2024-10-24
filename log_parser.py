# log_parser.py

import sys
import os
import re
import requests
import glob
from datetime import datetime
import pwd
from dotenv import load_dotenv

# Load environment variables from test.env file
load_dotenv('test.env')

# Read environment variables
LLM_API_URL = os.getenv('LLM_API_URL')
LOGREADER_USER = os.getenv('LOGREADER_USER')

# Debugging: Print environment variables to verify they are loaded
print(f"LLM_API_URL: {LLM_API_URL}")
print(f"LOGREADER_USER: {LOGREADER_USER}")

if not LLM_API_URL or not LOGREADER_USER:
    print("Environment variables LLM_API_URL and LOGREADER_USER must be set.")
    sys.exit(1)

# Function to switch to the 'logreader' user
def switch_to_logreader():
    try:
        logreader_uid = pwd.getpwnam(LOGREADER_USER).pw_uid
        os.setuid(logreader_uid)
    except KeyError:
        print(f"User '{LOGREADER_USER}' does not exist.")
        sys.exit(1)
    except PermissionError:
        print("Permission denied. This script must be run with root privileges to switch users.")
        sys.exit(1)

# Switch to 'logreader' user
switch_to_logreader()

# Assuming log date format is like 'YYYY-MM-DD HH:MM:SS'
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Define log levels
levels = {
    'INFO': 1,
    'WARNING': 2,
    'ERROR': 3,
    'CRITICAL': 4
}

# Directory to store temporary files
TMP_DIR = "/tmp/logreader"

def parse_log_line(line):
    """
    Parses a log line using a regex pattern to extract the timestamp, log level, and message.
    Returns a dictionary with the parsed components or None if the line doesn't match the pattern.
    """
    match = re.match(r'^(?P<timestamp>\S+) (?P<level>\S+): (?P<message>.+)$', line)
    if match:
        return match.groupdict()
    return None

def get_log_files():
    """
    Retrieves a list of log files from the /var/log/ directory.
    """
    return glob.glob('/var/log/*.log')

def parse_and_recommend(logs):
    """
    Filters logs based on log levels and sends them to an external API for recommendations.
    Returns a list of recommendations.
    """
    print("Parsing and recommending...")
    filtered_logs = [log for log in logs if levels.get(log['level'], 0) in [2, 3, 4]]
    print(f"Filtered logs: {filtered_logs}")
    
    try:
        response = requests.post(LLM_API_URL, json={"logs": filtered_logs})
        print(f"LLM API response status: {response.status_code}")
        
        if response.status_code == 200:
            recommendations = response.json().get("recommendations", [])
        else:
            recommendations = ["Error: Unable to get recommendations from LLM."]
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to LLM API: {e}")
        recommendations = ["Error: Unable to connect to LLM API."]
    
    return recommendations

def main():
    """
    Main function to start the log parser.
    Retrieves log files, processes each file, parses log lines, writes parsed logs to a temporary file,
    and gets recommendations from the external API.
    """
    print("Starting log parser...")

    logs = []
    for log_file_path in get_log_files():
        print(f"Processing log file: {log_file_path}")
        try:
            with open(log_file_path, 'r') as f:
                for line in f:
                    log_entry = parse_log_line(line.strip())
                    if log_entry:
                        logs.append(log_entry)
        except PermissionError as e:
            print(f"Permission denied: {log_file_path}")
            continue
    
    print(f"Parsed logs: {logs}")

    # Ensure the TMP_DIR exists
    if not os.path.exists(TMP_DIR):
        os.makedirs(TMP_DIR)

    # Write logs to temporary directory
    tmp_file_path = os.path.join(TMP_DIR, "parsed_logs.json")
    try:
        with open(tmp_file_path, 'w') as tmp_file:
            tmp_file.write(str(logs))
    except PermissionError as e:
        print(f"Permission denied: {tmp_file_path}")
        return
    
    recommendations = parse_and_recommend(logs)
    for rec in recommendations:
        print(rec)

if __name__ == "__main__":
    main()