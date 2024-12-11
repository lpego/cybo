# %% 
import pandas as pd
import re
import os

### Provide file name here
registrations = "..\website_exports\cybo-webinars-2024-registration-2024-12-04_10_07_56.csv"
conference_attendance = "..\website_exports\cybo-2025-registration,-attendance-only-2024-12-04_10_08_08.csv"
conference_contribution = "..\website_exports\cybo-2025-registration,-with-contribution-2024-12-04_10_08_04.csv"

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