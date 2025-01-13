### This script uses various exports to collect all user emails
### useful for sending newsletters, etc. 

# %% 
import pandas as pd
import re
import os
from glob import glob
from latest_file import find_most_recent_file

### Provide file name here
registrations = find_most_recent_file(glob("..\website_exports\cybo-webinars-2024-registration*[!A-z].csv"))
conference_attendance = find_most_recent_file(glob("..\website_exports\cybo-2025-registration,-attendance-only*[!A-z].csv")) 
conference_contribution = find_most_recent_file(glob("..\website_exports\cybo-2025-registration,-with-contribution*[!A-z].csv")) 

# %% 
email_list = []
for file in [registrations, conference_attendance, conference_contribution]: 
    data = pd.read_csv(file, skipinitialspace=True)
    data.columns = data.columns.str.strip()
    try: 
        # print(data["Email address"])
        email_list.extend(data["Email address"])
    except: 
        # print(data["User Email"])
        email_list.extend(data["User Email"])
# print(email_list)
print(len(email_list))
print(type(email_list))

### Convert to set ot remove duplicates, if any
email_set = set(email_list)
print(len(email_set))

with open("..\website_exports\email_list.txt", "w", encoding="utf-8") as file:
    for line in email_set: 
        file.write(f"{line}\n")

# %%
