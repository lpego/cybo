import re
from datetime import datetime

def find_most_recent_file(files):
    # Regular expression to match multiple timestamp formats
    timestamp_regex = re.compile(
        r"(?:[-_](\d{4}-\d{2}-\d{2}[_\d{2}_\d{2}_\d{2}]+)|_(\d{2}[A-Za-z]{3}\d{4}))\.csv$"
    )

    def extract_timestamp(file_name):
        match = timestamp_regex.search(file_name)
        if match:
            # Handle format: YYYY-MM-DD_HH_MM_SS
            if match.group(1):
                timestamp_str = match.group(1).replace("_", " ")
                return datetime.strptime(timestamp_str, "%Y-%m-%d %H %M %S")
            # Handle format: DDMMMYYYY
            elif match.group(2):
                timestamp_str = match.group(2)
                return datetime.strptime(timestamp_str, "%d%b%Y")
        return None

    # Parse timestamps for all files and keep track of the most recent one
    most_recent_file = None
    most_recent_time = None

    for file in files:
        timestamp = extract_timestamp(file)
        if timestamp:
            if not most_recent_time or timestamp > most_recent_time:
                most_recent_file = file
                most_recent_time = timestamp

    return most_recent_file

# # Example usage
# files = [
#     "cybo-2025-registration,-with-contribution-2024-12-09_16_18_43.csv",
#     "cybo_2025_registration_with_contribution_2024-12-10_14_15_01.csv",
#     "wp_users_10Dec2024.csv",
#     "wp_users_11Dec2024.csv"
# ]

# most_recent = find_most_recent_file(files)
# print(f"Most recent file: {most_recent}")
