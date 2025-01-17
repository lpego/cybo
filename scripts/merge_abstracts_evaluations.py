### This script merges the abstracts and reviewers' evaluations

# %% 
import pandas as pd
import re
import os
from glob import glob
from latest_file import find_most_recent_file
import datetime

# %% Read in most recent version of abstracts evaluations (i.e. Dashboard > Everest Forms > Entries > Export CSV)
filelist = glob("..\website_exports\evf-entry-export-abstract-evaluation-*.csv")
filename = find_most_recent_file(filelist) # grab most recent version
print("Reading from file: ", filename)
evaluations = pd.read_csv(filename, skipinitialspace=True)
evaluations = evaluations.rename(columns=lambda x: x.strip())
evaluations = evaluations.map(lambda x: x.strip() if isinstance(x, str) else x)
evaluations = evaluations.drop(["Date Created", "User Device", "User IP Address"], axis=1)

# %% Read in most recent version of abstracts (i.e. Dashboard > User Registration > Settings > Import/Export > Export users)
filelist = glob("..\website_exports\cybo-2025-registration,-with-contribution*[_redux].csv")
filename = find_most_recent_file(filelist) # grab most recent version
print("Reading from file: ", filename)
abstracts = pd.read_csv(filename, skipinitialspace=True)
abstracts = abstracts.rename(columns=lambda x: x.strip())
abstracts = abstracts.map(lambda x: x.strip() if isinstance(x, str) else x)
abstracts = abstracts.drop("Unnamed: 0", axis=1)

# %% Read in reviewer and handler info 
### from: https://docs.google.com/spreadsheets/d/1BMadWzY4oZoWmt86lfRpSVISu-6Q0NlssU-PvO2IiCE/edit?gid=55512928#gid=55512928
filename = ("..\website_exports\Abstracts list for evaluation - data_redux_parsed_FINAL.csv")
print("Reading from file: ", filename)
emails = pd.read_csv(filename, skipinitialspace=True)
emails = emails.rename(columns=lambda x: x.strip())
emails = emails.map(lambda x: x.strip() if isinstance(x, str) else x)
emails = emails.drop(['Unnamed: 0', 'First Name', 'Last Name', 'Email address',
       'Career stage', 'Country', 'Gender',
       'What type of contribution would you prefer to submit?',
       'Preferred session', 'Alternative session', 'User Registered GMT',
       'user_email', 'user_login'], axis=1)

# %% Merge by URL
merged = abstracts.merge(evaluations, left_on="URL", right_on="Link to the abstract", how="left")
merged = merged.drop("Link to the abstract", axis=1)
merged = merged.merge(emails, on="URL", how="left")
# merged = merged.drop("Link to the abstract", axis=1)

# %% Find suggested up / down-grades
# Filter rows where both columns have non-empty values
filtered = merged.dropna(subset=["What type of contribution would you prefer to submit?", "Reccommended type of contribution"])
# Find rows where the values are different
different_contributions = filtered[filtered["What type of contribution would you prefer to submit?"] != filtered["Reccommended type of contribution"]]
# Display the result
print(different_contributions)

# %% Add "Reviewed?" column based on "Status" column
merged["Reviewed?"] = merged["Status"].apply(lambda x: "✔" if pd.notna(x) and x != "" else "")

# %% Write out to file
current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
merged.to_csv(f"..\website_exports\merged_abstracts_evaluations_{current_datetime}.csv")

# %%
