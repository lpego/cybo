### This script parses the abstracts form export, cleans rogue newlines, 
### and writes out a reduced csv for further processing

# %% 
import pandas as pd
import re
import os
import csv
from glob import glob
from latest_file import find_most_recent_file

### Provide file lists here here
filelist = glob("..\website_exports\cybo-2025-registration,-with-contribution*[!A-z].csv")
filename = find_most_recent_file(filelist) # grab most recent version
print("Reading from file: ", filename)

# %% Replace pandas read_csv with csv module for better handling of quoted fields
with open(filename, mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    rows = list(reader)
# Convert the rows back to a pandas DataFrame
data = pd.DataFrame(rows)
# Ensure all fields are stripped of rogue newlines
data = data.applymap(lambda x: str(x).replace('\n', ' ') if isinstance(x, str) else x)

# %% count preferred sessions
data['Preferred session'].value_counts()
talks  = data[data["What type of contribution would you prefer to submit?"] == "Talk"]
talks['Preferred session'].value_counts()
# %% count preferred sessions
data["What type of contribution would you prefer to submit?"].value_counts()
# %% gender balance
data['Gender'].value_counts()
# %% career stage
data['Career stage'].value_counts()

# %% suggestions changes


# %%
### Prepare reduced version
data_redux = data
# data_redux = data[['First Name', 'Last Name', 'Email address', 'Career stage', 'Country', 'Gender',
#        'What type of contribution would you prefer to submit?', 'Preferred session', 'Alternative session', 'User Registered GMT', 
#        'Title', "Contributing author's institution"]]
# ### Obtain usernames based on email addresses - CAUTION! some users have different usernames...
# data_redux["Username"] = data['Email address'].str.extract(r'^([^@]+)@')
### Sort by registration date
data_redux['User Registered GMT'] = pd.to_datetime(data_redux['User Registered GMT'])
data_redux = data_redux.sort_values('User Registered GMT', ascending=True)

# %%
### Grab full user table from the phpMyAdmin database manager
### Look for the table "wp_users" and export as .csv
wp_users = pd.read_csv(find_most_recent_file(glob("..\website_exports\wp_users*")))
print("Reading user table from file: ", find_most_recent_file(glob("..\website_exports\wp_users*")))
### Merge by email
data_redux_merged = data_redux.merge(wp_users[['user_email', 'user_login']], left_on='Email address', right_on='user_email', how='left')
### Make URL
data_redux_merged["URL"] = 'https://conferenceyoungbotanists.com/abstracts/' + data_redux_merged['user_login']

### write out to file
print(
       "Writing out: ", 
       # os.path.splitext(filename)[0]+"_parsed.csv", " ; ", 
       os.path.splitext(filename)[0]+"_redux.csv"
       )
# data.to_csv(os.path.splitext(filename)[0]+"_parsed.csv")
data_redux_merged.to_csv(os.path.splitext(filename)[0]+"_redux.csv")

# %% 
### EXTRA: merge back to existing reviewer assignments from Google Sheet
gsheet = pd.read_csv("..\website_exports\Abstracts list for evaluation - data_redux_parsed.csv")
gsheet = gsheet[["Email address", "Reviewer", "Handler", "Reviewed?", "Notes", "Reviewer_email", "Handler_email"]]
gsheet_new = data_redux_merged.merge(gsheet, on="Email address", how="outer")
gsheet_new['User Registered GMT'] = pd.to_datetime(gsheet_new['User Registered GMT'])
gsheet_new.sort_values('User Registered GMT', ascending=True)
gsheet_new.to_csv("..\website_exports\Abstracts list for evaluation - data_redux_parsed_NEW.csv")

# %%
