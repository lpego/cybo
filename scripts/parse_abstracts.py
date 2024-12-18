import pandas as pd
import re
import os
from glob import glob
from latest_file import find_most_recent_file

### Provide file lists here here
filelist = glob("..\website_exports\cybo-2025-registration,-with-contribution*[!A-z].csv")
filename = find_most_recent_file(filelist) # grab most recent version
print("Reading from file: ", filename)

data = pd.read_csv(filename)

# Strip newlines from all cells
data = data.apply(lambda x: str(x).replace('\n', ' ') if isinstance(x, str) else x)

### count preferred sessions
data['Preferred session'].value_counts()
### gender balance
data['Gender'].value_counts()

### Prepare reduced version
data_redux = data[['First Name', 'Last Name', 'Email address', 'Career stage', 'Country', 'Gender',
       'What type of contribution would you prefer to submit?', 'Preferred session', 'Alternative session']]
# ### Obtain usernames based on email addresses - CAUTION< some users have different usernames...
# data_redux["Username"] = data['Email address'].str.extract(r'^([^@]+)@')

### Grab full user table
# wp_users = pd.read_csv("..\website_exports\wp_users_10Dec2024.csv")
wp_users = pd.read_csv(find_most_recent_file(glob("..\website_exports\wp_users*")))
print("Reading user table from file: ", find_most_recent_file(glob("..\website_exports\wp_users*")))
### Merge by email
data_redux = data_redux.merge(wp_users[['user_email', 'user_login']], left_on='Email address', right_on='user_email', how='left')
### Make URL
data_redux["URL"] = 'https://conferenceyoungbotanists.com/abstracts/' + data_redux['user_login']

### write out to file
print("Writing out: ", os.path.splitext(filename)[0]+"_parsed.csv", " ; ", os.path.splitext(filename)[0]+"redux.csv")
data.to_csv(os.path.splitext(filename)[0]+"_parsed.csv")
data_redux.to_csv(os.path.splitext(filename)[0]+"_redux.csv")
