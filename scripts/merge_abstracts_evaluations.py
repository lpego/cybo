### This script merges the abstracts and reviewers' evaluations

# %% 
import pandas as pd
import re
import os
from glob import glob
from latest_file import find_most_recent_file

# %% Read in most recent version of abstracts evaluations (i.e. Dashboard > Everest Forms > Entries > Export CSV)
filelist = glob("..\website_exports\evf-entry-export-abstract-evaluation-*.csv")
filename = find_most_recent_file(filelist) # grab most recent version
print("Reading from file: ", filename)
evaluations = pd.read_csv(filename)
evaluations = evaluations.drop(["Date Created", "User Device", "User IP Address"], axis=1)

# %% Read in most recent version of abstracts (i.e. Dashboard > User Registration > Settings > Import/Export > Export users)
filelist = glob("..\website_exports\cybo-2025-registration,-with-contribution*[_redux].csv")
filename = find_most_recent_file(filelist) # grab most recent version
print("Reading from file: ", filename)
abstracts = pd.read_csv(filename)
abstracts = abstracts.drop("Unnamed: 0", axis=1)

# %%
### Merge by URL
merged = abstracts.merge(evaluations, left_on="URL", right_on="Link to the abstract", how="left")
merged = merged.drop("Link to the abstract", axis=1)

# %%
### write out to file
merged.to_csv("..\website_exports\merged_abstracts_evaluations.csv")

# %%
