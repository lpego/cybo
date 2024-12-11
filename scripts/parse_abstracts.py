import pandas as pd
import re
import os

### Provide file name here
filename = "..\website_exports\cybo-2025-registration,-with-contribution-2024-12-09_16_18_43.csv"

data = pd.read_csv(filename)

# Strip newlines from all cells
data = data.apply(lambda x: str(x).replace('\n', ' ') if isinstance(x, str) else x)

### count preferred sessions
data['Preferred session'].value_counts()
data['Gender'].value_counts()

### Prepare reduced version
data_redux = data[['First Name', 'Last Name', 'Email address', 'Career stage', 'Country', 'Gender',
       'What type of contribution would you prefer to submit?', 'Preferred session', 'Alternative session']]
# ### Obtain usernames based on email addresses - CAUTION< some users have different usernames...
# data_redux["Username"] = data['Email address'].str.extract(r'^([^@]+)@')

### Grab full user table
wp_users = pd.read_csv("..\website_exports\wp_users_10Dec2024.csv")
### Merge by email
data_redux = data_redux.merge(wp_users[['user_email', 'user_login']], left_on='Email address', right_on='user_email', how='left')
### Make URL
data_redux["URL"] = 'https://conferenceyoungbotanists.com/abstracts/' + data_redux['user_login']

### write out to file
data.to_csv(os.path.splitext(filename)[0]+"_parsed.csv")
data_redux.to_csv("..\\website_exports\\abstracts_redux_parsed.csv")
