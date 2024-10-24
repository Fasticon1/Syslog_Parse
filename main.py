import glob
import re
import os
import subprocess
import sys
import logging
from datetime import datetime

# Assuming log date format is like 'YYYY-MM-DD HH:MM:SS'
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

def query_syslogs(pattern, date_pattern=None):
    log_files = glob.glob('/var/log/*.log')
    if not log_files:
        print("No log files found in /var/log/")
        return
    
    regex = re.compile(pattern, re.IGNORECASE)
    found = False
    
    for log_file in log_files:
        if os.path.isfile(log_file):
            with open(log_file, 'r') as file:
                for line in file:
                    if regex.search(line):
                        if date_pattern:
                            try:
                                log_date = extract_date_from_line(line)
                                if log_date and log_date.startswith(date_pattern):
                                    print(line.strip())
                                    found = True
                            except ValueError:
                                continue
                        else:
                            print(line.strip())
                            found = True
    
    if not found:
        print("No matches found for pattern:", pattern)

def extract_date_from_line(line):
    try:
        log_date_str = line.split()[0] + ' ' + line.split()[1]
        log_date = datetime.strptime(log_date_str, DATE_FORMAT)
        return log_date.strftime("%Y-%m-%d")
    except (ValueError, IndexError):
        return None

# Enhanced Exception Handling
try:
    # Code to read and parse logs
    pass
except (ValueError, IndexError, FileNotFoundError, PermissionError) as e:
    logging.error(f"An error occurred: {e}")

# Log Level Filtering
def filter_logs(logs, level):
    levels = {'INFO': 1, 'WARNING': 2, 'ERROR': 3}
    return [log for log in logs if levels[log['level']] >= levels[level]]

# Keyword Search
def search_logs(logs, keyword):
    return [log for log in logs if keyword in log['message']]

# Timestamp Parsing
def parse_timestamp(log_entry):
    try:
        timestamp_str = log_entry.split()[0]
        if len(log_entry.split()) > 1:
            timestamp_str += ' ' + log_entry.split()[1]
        else:
            timestamp_str += ' 00:00:00'  # Default to midnight if time is missing
        return datetime.strptime(timestamp_str, DATE_FORMAT)
    except (ValueError, IndexError) as e:
        logging.error(f"Error parsing timestamp: {e}")
        return None

# Alerting System
def alert_on_pattern(logs, pattern):
    for log in logs:
        if re.search(pattern, log['message']):
            send_alert(log)

def send_alert(log):
    # Code to send alert (e.g., email, SMS)
    pass

def main():
    if os.geteuid() != 0:
        print("Re-running script with sudo...")
        try:
            subprocess.check_call(['sudo', sys.executable] + sys.argv)
        except subprocess.CalledProcessError as e:
            print(f"Failed to run script with sudo: {e}")
        return
    
    print("Enter a search term (e.g., 'error', 'failed', 'warning'):")
    search_term = input("Search Pattern: ").strip()
    
    print("Enter the dates you wish to search (YYYY-MM-DD) or leave blank to search all dates (e.g., '2023-10-01'):")
    date_pattern = input("Date Pattern: ").strip()
    
    query_syslogs(search_term, date_pattern if date_pattern else None)

if __name__ == "__main__":
    main()

# Example usage
if __name__ == "__main__":
    logs = [
        {'timestamp': '2023-10-01 12:00:00', 'level': 'ERROR', 'message': 'Disk space low'},
        {'timestamp': '2023-10-01', 'level': 'INFO', 'message': 'System rebooted'}
    ]

    filtered_logs = filter_logs(logs, 'WARNING')
    keyword_logs = search_logs(logs, 'Disk')
    for log in logs:
        log['parsed_timestamp'] = parse_timestamp(log['timestamp'])
    alert_on_pattern(logs, 'Disk space low')