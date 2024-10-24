# Syslog Query Script

This Python script allows you to query syslog files in the `/var/log/` directory for specific patterns and dates.

## Prerequisites

- Python 3.x
- Root privileges (the script will prompt for `sudo` if not run as root)

## Usage

1. Clone the repository or download the script.
2. Run the script using Python:

    ```sh
    python3 main.py
    ```

3. Follow the prompts:
    - **Search Term**: Enter the term you want to search for (e.g., `error`, `failed`, `warning`).
    - **Date Pattern**: Enter the date in `YYYY-MM-DD` format to filter logs by date (e.g., `2023-10-01`). Leave blank to search all dates.

## Example

```sh
Enter a search term (e.g., 'error', 'failed', 'warning'):
Search Pattern: error
Enter the dates you wish to search (YYYY-MM-DD) or leave blank to search all dates (e.g., '2023-10-01'):
Date Pattern: 2023-10-01


# LOG PARSER SCRIPT

### Overview

Designed to parse log files from the log directory, filter them based on log levels, and send the filtered logs to an external API for recommendations.

### Usage

To run the script, use the following command:

```sh
sudo python /path/to/log_parser.py
```

### Warning

**Note:** This script is currently a work in progress and may be incomplete. Use it with caution and be aware that it might not function as expected.


### Dependencies

The script requires the following Python packages:
- `requests`

You can install the dependencies using `pip`:

```sh
pip install requests
```

### Contributing

Contributions to improve this script are welcome. Please submit a pull request or open an issue to discuss any changes.

