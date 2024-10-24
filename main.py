import glob
import re
import os
import subprocess
import sys
from datetime import datetime

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
    # Assuming log date format is like 'YYYY-MM-DD HH:MM:SS'
    date_format = "%Y-%m-%d %H:%M:%S"
    try:
        log_date_str = line.split()[0] + ' ' + line.split()[1]
        log_date = datetime.strptime(log_date_str, date_format)
        return log_date.strftime("%Y-%m-%d")
    except (ValueError, IndexError):
        return None

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