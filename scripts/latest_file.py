import re
from datetime import datetime

def find_most_recent_file(files):
    timestamp_regex = re.compile(
        r"(\d{4}-\d{2}-\d{2}_\d{2}_\d{2}_\d{2})"  # Format: YYYY-MM-DD_HH_MM_SS
        r"|(\d{4}-\d{2}-\d{2})"  # Format: YYYY-MM-DD
        r"|(\d{2}[A-Za-z]{3}\d{4})"  # Format: DDMMMYYYY
    )

    def extract_timestamp(file_name):
        match = timestamp_regex.search(file_name)
        if match:
            # Handle format: YYYY-MM-DD_HH_MM_SS
            if match.group(1):
                timestamp_str = match.group(1).replace("_", " ")
                return datetime.strptime(timestamp_str, "%Y-%m-%d %H %M %S")
            # Handle format: YYYY-MM-DD
            elif match.group(2):
                timestamp_str = match.group(2)
                return datetime.strptime(timestamp_str, "%Y-%m-%d")
            # Handle format: DDMMMYYYY
            elif match.group(3):
                timestamp_str = match.group(3)
                return datetime.strptime(timestamp_str, "%d%b%Y")
        return None

    # Iterate through files and determine the most recent
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
#     "wp_users_11Dec2024.csv",
#     "cybo-2025-registration,-with-contribution-2024-12-18_11_29_37_redux.csv",
#     "wp_users_22Dec2024.csv",
#     "cybo-2025-registration,-with-contribution-2024-12-23_11_29_37_redux.csv",
#     "evf-entry-export-abstract-evaluation-2024-12-11-9622391a024e2387a88157a78094f283.csv", 
#     "evf-entry-export-abstract-evaluation-2025-01-06-9622391a024e2387a88157a78094f283.csv",
# ]

# most_recent = find_most_recent_file(files)
# print(f"Most recent file: {most_recent}")
